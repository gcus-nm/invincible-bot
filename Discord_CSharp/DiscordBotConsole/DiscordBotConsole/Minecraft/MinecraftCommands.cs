using Discord.Commands;
using System;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace DiscordBotConsole.Minecraft
{
	/// <summary>
	/// マイクラ関連のコマンド情報がまとまっている
	/// </summary>
	[Group("minecraft")]
	[Alias("mine")]
	public class MinecraftCommands : ModuleBase
	{
		// サーバー設定
		private const string SERVER_ADDRESS = "gcus-MacPro.local";
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
			if (await IsConnetcionServer())
			{
				await ReplyAsync("すでにサーバーは起動しています。");
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

			BotUtility.ShellStartForEnvironment($"bash /Users/user/minecraft/Git/build.sh {serverVersion} {useRam} {info.JavaVersion}");

			try
			{
				await BotUtility.WaitWhile(IsConnetcionServer());
			}
			catch (TimeoutException)
			{
				await ReplyAsync("サーバーを起動できませんでした。");
				return;
			}

			await ReplyAsync("サーバーが起動しました！");
		}
		
		/// <summary>
		/// 起動できるサーバーの一覧を表示する
		/// </summary>
		/// <returns></returns>
		[Command("ServerList")]
		[Alias("list")]
		public async Task DisplayServerList()
		{
			StringBuilder serverList = new StringBuilder();
			serverList.AppendLine("有効なサーバー一覧");
			for (int i = 0; i < MinecraftServerData.MINECRAFT_SERVERS.Length; ++i)
			{
				var server = MinecraftServerData.MINECRAFT_SERVERS[i];
				serverList.Append($"- サーバー名 ：{server.ServerFriendlyName}\t 起動名：");

				for (int j = 0; j < server.BuildServerTexts.Length; ++j)
				{
					if (j != 0)
					{
						serverList.Append(", ");
					}
					serverList.Append($"{server.BuildServerTexts[j]}");
				}
			}
			serverList.AppendLine();

			await ReplyAsync(serverList.ToString());
		}

		/// <summary>
		/// サーバーのTCPポートに接続できるかを確認する（サーバーが立っているか）
		/// </summary>
		/// <returns></returns>
		private async Task<bool> IsConnetcionServer()
		{
			try
			{
				// クライアント作成
				using (var tcpClient = new TcpClient())
				{
					// 送受信タイムアウト設定
					tcpClient.SendTimeout = 1000;
					tcpClient.ReceiveTimeout = 1000;

					try
					{
						// サーバーへ接続開始
						await tcpClient.ConnectAsync(SERVER_ADDRESS, SERVER_PORT);
					}
					catch (ObjectDisposedException)
					{
						Console.WriteLine("接続失敗！");
						return false;
					}

					return true;
				}
			}
			catch (Exception ex)
			{
				Console.WriteLine(ex.ToString());
				throw ex;
			}
		}
	}
}
