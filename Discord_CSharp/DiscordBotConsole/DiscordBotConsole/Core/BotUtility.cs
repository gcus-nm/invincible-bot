using Discord.WebSocket;
using System;
using System.Diagnostics;
using System.Threading.Tasks;

namespace DiscordBotConsole
{
	public static class BotUtility
	{
		/// <summary>
		/// メッセージが有効かどうか
		/// </summary>
		/// <param name="message"></param>
		/// <returns></returns>
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

		/// <summary>
		/// 環境によって自動的にShell実行を切り替える
		/// </summary>
		/// <param name="shellFilePath"></param>
		/// <returns></returns>
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
		/// WindowsでShell実行
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
		/// macOSでShell実行
		/// </summary>
		/// <param name="shellFilePath"></param>
		/// <returns></returns>
		public static Process ShellStartForMac(string command)
		{
			var shell = new ProcessStartInfo()
			{
				FileName = "osascript",
				Arguments = $"-e 'tell application \"Terminal\" to activate' -e 'tell application \"Terminal\" to do script \"{command}\"'",

				UseShellExecute = true,
				CreateNoWindow = false,
				Verb = "runas",
				RedirectStandardOutput = false,
				RedirectStandardInput = false,
			};

			return Process.Start(shell);
		}

		/// <summary>
		/// 条件がTrueの間、待ち続ける
		/// </summary>
		/// <param name="status">whileループに利用する条件</param>
		/// <param name="timeout">タイムアウト時間</param>
		/// <param name="checkInterval">条件式の確認間隔</param>
		/// <returns></returns>
		public static async Task WaitWhile(Func<bool> status, int timeout = 30000, int checkInterval = 100)
		{
			int loopLimit = timeout / checkInterval;
			for (int i = 0; i < loopLimit; ++i)
			{
				if (!status.Invoke())
				{
					return;
				}

				await Task.Delay(100);
			}

			throw new TimeoutException();
		}
	}
}
