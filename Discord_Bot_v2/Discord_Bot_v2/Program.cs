using Discord;
using Discord.Commands;
using Discord.WebSocket;
using System;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using System.Reflection;

namespace Discord_Bot_v2
{	class Program
	{
		private DiscordSocketClient m_Client;
		public static CommandService m_Command;
		public static IServiceProvider m_Services;
		public static void Main(string[] args)
			=> new Program().InitializeAsync().GetAwaiter().GetResult();

		public async Task InitializeAsync()
		{
			m_Client = new DiscordSocketClient(new DiscordSocketConfig
			{
				LogLevel = LogSeverity.Info
			});

			m_Client.Log += Log;
			m_Command = new CommandService();
			m_Services = new ServiceCollection().BuildServiceProvider();

			await InitCommands();

			string token = Environment.GetEnvironmentVariable("DISCORD_TOKEN");
			await m_Client.LoginAsync(TokenType.Bot, token);
			await m_Client.StartAsync();

			// 無限ループって怖くね？
			await Task.Delay(-1);
		}

		/// <summary>
		/// コマンドを呼び出すための初期化
		/// </summary>
		private async Task InitCommands()
		{
			await m_Command.AddModulesAsync(Assembly.GetEntryAssembly(), m_Services);
			m_Client.MessageReceived += HandleCommandAsync;
		}

		/// <summary>
		/// ろがー
		/// </summary>
		/// <param name="logMessage"></param>
		/// <returns></returns>
		private Task Log(LogMessage logMessage)
		{
			Console.WriteLine(logMessage.Message);
			return Task.CompletedTask;
		}

		/// <summary>
		/// コマンドの基盤
		/// </summary>
		/// <param name="_message">メッセージ内容</param>
		private async Task HandleCommandAsync(SocketMessage _message)
		{
			// システムメッセージを弾く
			var message = _message as SocketUserMessage;
			if (message == null)
			{
				return;
			}

			// Bot拒否
			if (message.Author.IsBot)
			{
				return;
			}

			Console.WriteLine($"送信者：{message.Author.Username} 内容：{message.Content}");

			int pos = 0;

			if (message.HasCharPrefix('!', ref pos))
			{
				var context = new SocketCommandContext(m_Client, message);

				await m_Command.ExecuteAsync(context, pos, m_Services);
			}
		}
	}
}
