using Discord.WebSocket;
using System.Diagnostics;

namespace DiscordBotConsole
{
	public static class BotUtility
	{
		public static bool IsValidMessage(SocketMessage message)
		{
			if (message == null)
			{
				return false;
			}

			if (message.Author.IsBot)
			{
				return false;
			}

			return true;
		}

		public static Process ShellStartForEnvironment(string shellFilePath)
		{
			if (System.Runtime.InteropServices.RuntimeInformation.IsOSPlatform(System.Runtime.InteropServices.OSPlatform.Windows))
			{
				return ShellStartForWindows(shellFilePath);
			}
			else if (System.Runtime.InteropServices.RuntimeInformation.IsOSPlatform(System.Runtime.InteropServices.OSPlatform.OSX))
			{
				return ShellStartForMac(shellFilePath);
			}
			else
			{
				throw new System.InvalidOperationException();
			}
		}

		/// <summary>
		/// Windowsでshを実行
		/// </summary>
		/// <param name="shellFilePath"></param>
		/// <returns></returns>
		public static Process ShellStartForWindows(string command)
		{
			var terminalPath = "cmd.exe";

			var shell = new ProcessStartInfo(terminalPath, $"/k {command}");

			return Process.Start(shell);
		}

		/// <summary>
		/// macOSでshを実行
		/// </summary>
		/// <param name="shellFilePath"></param>
		/// <returns></returns>
		public static Process ShellStartForMac(string command)
		{
			var terminalPath = "/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal";

			var shell = new ProcessStartInfo(terminalPath, command);

			return Process.Start(shell);
		}
	}
}
