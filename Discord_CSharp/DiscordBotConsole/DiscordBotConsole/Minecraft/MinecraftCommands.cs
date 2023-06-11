﻿using CoreRCON;
using Discord.Commands;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace DiscordBotConsole.Minecraft
{
	public enum ServerConnectionType 
	{
		Client,
		RCON,
	}

	/// <summary>
	/// マイクラ関連のコマンド情報がまとまっている
	/// </summary>
	[Group("minecraft")]
	[Alias("mine")]
	public class MinecraftCommands : ModuleBase
	{
		// サーバー設定
		private const string SERVER_HOSTNAME = "gcus-MacPro.local";
		private const string SERVER_IP_ADDRESS = "127.0.0.1";
		private const int SERVER_PORT = 25024;
		private const string RCON_PASSWORD = "2126";
		private const int RCON_PORT = 25025;
		private const int DEFAULT_USE_RAM = 12;

		// バージョン等指定
		private const string DEFAULT_VERSION = "1.20.0";

		private bool m_IsRunningMinecraft = false;

		/// <summary>
		/// サーバーを起動する
		/// </summary>
		/// <param name="serverVersion"></param>
		/// <param name="useRam"></param>
		/// <returns></returns>
		[Command("start")]
		public async Task StartServer(string serverVersion = DEFAULT_VERSION, int useRam = DEFAULT_USE_RAM)
		{
			await ReplyAsync("サーバーの起動状態を確認しています...");

			if (await IsConnetcionServer(ServerConnectionType.Client))
			{
				await ReplyAsync("すでにサーバーが起動しているため、新たに起動できません。");
				return;
			}

			var info = MinecraftServerData.MINECRAFT_SERVERS.FirstOrDefault(server => server.BuildServerTexts.Any(version => version.Contains(serverVersion)));

			if (info == null)
			{
				await ReplyAsync($"指定されたバージョン {serverVersion} がサーバーで見つかりません。");

				await DisplayServerList();

				return;
			}

			await ReplyAsync($"{info.ServerFriendlyName} の起動を開始します...");

			string command = BotUtility.GetValueFromOS(new KeyValuePair<OSPlatform, string>[]
			{
				new KeyValuePair<OSPlatform, string>(OSPlatform.OSX, $"bash /Users/user/minecraft/Git/MinecraftBuild.sh {serverVersion} {useRam} {info.JavaVersion}"),
			});

			BotUtility.ShellStartForEnvironment(command);

			bool isConnected = false;
			for (int i = 0; i < 60; ++i)
			{
				isConnected = await IsConnetcionServer(ServerConnectionType.RCON);
				if (isConnected)
				{
					break;
				}

				await Task.Delay(1000);
			}

			if (isConnected)
			{
				await ReplyAsync("サーバーが起動しました！");
			}
			else
			{
				await ReplyAsync("時間内にサーバーを起動できませんでした。");
			}

			var _ = ServerSurveillance(ReplyAsync("サーバーが停止しました。"));
		}

		/// <summary>
		/// サーバーを停止する
		/// </summary>
		/// <returns></returns>
		[Command("stop")]
		public async Task StopServer()
		{
			if (!await IsConnetcionServer(ServerConnectionType.Client))
			{
				await ReplyAsync("サーバーは起動していません。");
				return;
			}

			if (!await IsConnetcionServer(ServerConnectionType.RCON))
			{
				await ReplyAsync("サーバーにコマンドを送信できません。");
				return;
			}

			await ReplyAsync("サーバーを停止します...");
			await SendCommandInternal("stop");
		}
		
		/// <summary>
		/// サーバーの状態を表示する
		/// </summary>
		/// <returns></returns>
		[Command("status")]
		[Alias("stat")]
		public async Task DisplayServerStatus()
		{
			string displayText = "サーバーは起動していません。";

			if (await IsConnetcionServer(ServerConnectionType.Client))
			{
				displayText = "サーバーは起動しています。";
			}
			
			await ReplyAsync(displayText);
		}


		/// <summary>
		/// rconでコマンド送信する
		/// </summary>
		/// <param name="command"></param>
		/// <param name="commandArgs"></param>
		/// <returns></returns>
		[Command("command")]
		[Alias("cmd")]
		public async Task SendCommand(string command, params string[] args)
		{
			if (!await IsConnetcionServer(ServerConnectionType.Client))
			{
				await ReplyAsync("サーバーは起動していません。");
				return;
			}

			if (!await IsConnetcionServer(ServerConnectionType.RCON))
			{
				await ReplyAsync("サーバーにコマンドを送信できません。");
				return;
			}

			if (string.IsNullOrEmpty(command))
			{
				await ReplyAsync("コマンドを入力してください。");
			}

			string result = await SendCommandInternal(command, args);
			string format = string.IsNullOrEmpty(result) ? "コマンド送信成功" : $"コマンド結果：{result}";

			Console.WriteLine(format);
			await ReplyAsync(format);
		}		
		
		/// <summary>
		/// 起動できるサーバーの一覧を表示する
		/// </summary>
		/// <returns></returns>
		[Command("serverlist")]
		[Alias("list")]
		public async Task DisplayServerList()
		{
			StringBuilder serverList = new StringBuilder();
			serverList.AppendLine("有効なサーバー一覧");
			for (int i = 0; i < MinecraftServerData.MINECRAFT_SERVERS.Length; ++i)
			{
				var server = MinecraftServerData.MINECRAFT_SERVERS[i];
				serverList.Append($"- サーバー名 ：{server.ServerFriendlyName}\t\t 起動名：");

				for (int j = 0; j < server.BuildServerTexts.Length; ++j)
				{
					if (j != 0)
					{
						serverList.Append(", ");
					}
					serverList.Append($"「{server.BuildServerTexts[j]}」");
				}
				serverList.AppendLine();
			}

			await ReplyAsync(serverList.ToString());
		}

		/// <summary>
		/// サーバーの終了を監視する
		/// </summary>
		/// <param name="surveillanceInterval"></param>
		/// <returns></returns>
		private Task ServerSurveillance(Task onCloseServerTask, int surveillanceInterval = 3000)
		{
			return Task.Run(() =>
			{
				bool isOnceConnected = false;
				while (true)
				{
					bool isConnect = IsConnetcionServer(ServerConnectionType.Client).Result;
					if (isConnect)
					{
						Console.WriteLine("Surveillance Start");
						isOnceConnected = true;
					}
					else if (isOnceConnected && !isConnect)
					{
						Console.WriteLine("Surveillance Break");
						break;
					}

					Task.Delay(surveillanceInterval).Wait();
				};
			}).ContinueWith((_) => onCloseServerTask.Wait());
		}

		/// <summary>
		/// rconでコマンド送信する（内部処理用）
		/// </summary>
		/// <param name="command"></param>
		/// <param name="args"></param>
		/// <returns></returns>
		private async Task<string> SendCommandInternal(string command, params string[] args)
		{
			var serveraddress = IPAddress.Parse(SERVER_IP_ADDRESS);

			var connection = new RCON(serveraddress, RCON_PORT, RCON_PASSWORD);

			StringBuilder commandBuilder = new StringBuilder(command);
			for (int i = 0; i < args.Length; ++i)
			{
				commandBuilder.Append($" {args[i]}");
			}

			var connectTask = connection.SendCommandAsync(commandBuilder.ToString());

			// サーバーへ接続開始
			if (await Task.WhenAny(connectTask, Task.Delay(1000)) != connectTask)
			{
				await ReplyAsync("コマンドを送信できませんでした。");
				return "コマンドを送信できませんでした。";
			}

			return await connectTask;
		}

		/// <summary>
		/// サーバーのTCPポートに接続できるかを確認する（サーバーが立っているか）
		/// </summary>
		/// <returns></returns>
		private async Task<bool> IsConnetcionServer(ServerConnectionType connectType, int timeout = 1000)
		{
			try
			{
				// クライアント作成
				using (var tcpClient = new TcpClient())
				{
					// 送受信タイムアウト設定
					tcpClient.SendTimeout = 1000;
					tcpClient.ReceiveTimeout = 1000;

					int port = 0;
					switch (connectType) 
					{
						case ServerConnectionType.Client:
							port = SERVER_PORT;
							break;

						case ServerConnectionType.RCON:
							port = RCON_PORT;
							break;
					}

					var connectTask = tcpClient.ConnectAsync(SERVER_HOSTNAME, port);

					// サーバーへ接続開始
					if (await Task.WhenAny(connectTask, Task.Delay(timeout)) != connectTask)
					{
						throw new TimeoutException($"{timeout}ms以内に接続できませんでした。");
					}

					return true;
				}
			}
			catch (SocketException socket)
			{
				Console.WriteLine($"{nameof(IsConnetcionServer)} でハンドリングしたSocketException\n----------\n{socket}\n----------\n");
				return false;
			}
			catch (TimeoutException time)
			{
				Console.WriteLine($"{nameof(IsConnetcionServer)} でハンドリングしたTimeoutException\n----------\n{time}\n----------\n");
				return false;
			}
			catch (Exception ex)
			{
				Console.WriteLine($"{nameof(IsConnetcionServer)} でキャッチした例外（未ハンドリング）\n----------\n{ex}\n----------\n");
				throw ex;
			}
		}
	}
}
