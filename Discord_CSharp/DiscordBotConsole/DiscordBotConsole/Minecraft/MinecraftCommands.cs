using Discord.Commands;
using System.Linq;
using System.Threading.Tasks;

namespace DiscordBotConsole.Minecraft
{
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

		[Command("start")]
		public async Task StartServer(string serverVersion = DEFAULT_VERSION, int useRam = DEFAULT_USE_RAM)
		{
			if (m_IsRunningMinecraft)
			{
				await ReplyAsync("すでにサーバーは起動しています。");
				return;
			}

			var info = MinecraftServerData.MINECRAFT_SERVERS.FirstOrDefault(server => server.BuildServerTexts.Any(version => version.Contains(serverVersion)));

			if (info == null)
			{
				await ReplyAsync($"指定されたバージョン {serverVersion} がサーバーで見つかりません。");
				return;
			}

			await ReplyAsync($"{info.ServerFriendlyName} の起動を開始します...");

			BotUtility.ShellStartForEnvironment($"bash /Users/user/minecraft/Git/build.sh {serverVersion} {useRam} {info.JavaVersion}");
		}
	}
}
