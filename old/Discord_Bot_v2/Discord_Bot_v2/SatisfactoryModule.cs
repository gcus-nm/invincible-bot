using Discord.Commands;
using System.Threading.Tasks;

namespace Discord_Bot_v2
{
	[Group("Satisfactory")]
	public class SatisfactoryModule : ModuleBase<SocketCommandContext>
	{
		[Command("test")]
		[Summary("テストだよ！")]
		public async Task TestAsync()
		{
			await Context.Channel.SendMessageAsync($"YEAH");
		}

		[Command("test2")]
		[Summary("テストだよ！")]
		public async Task TestAsync(
			[Summary("なにか")]
			int x)
		{
			await Context.Channel.SendMessageAsync($"WTF!! {x}");
		}
	}
}
