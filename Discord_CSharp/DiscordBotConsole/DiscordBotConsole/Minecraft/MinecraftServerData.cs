using System.Collections.Generic;
using System.Linq;

namespace DiscordBotConsole.Minecraft
{
	public class MinecraftServerData
	{
		public readonly static List<MinecraftServerData> MINECRAFT_SERVERS = new List<MinecraftServerData>()
		{
			new MinecraftServerData("1.12.2Mohist",			"1.12.2 匠サーバー",			8,		"takumi"),
			new MinecraftServerData("1.12.2SkyFactory4",	"1.12.2 SkyFactory4",			8,		"sky", "skyfactory" ),
			new MinecraftServerData("1.18.1P",				"1.18.1 軽量バニラサーバー",	17,		"1.18.1", "1.18.1P" ),
			new MinecraftServerData("1.19",					"1.19 バニラサーバー",			17,		"1.19.0", "1.19"),
			new MinecraftServerData("1.19.3",				"1.19.3 バニラサーバー",		17,		"1.19.3"),
			new MinecraftServerData("1.20.0",               "1.20.0 バニラサーバー",		17,		"1.20.0", "1.20"),
		};

		public MinecraftServerData(string serverName, string serverFriendlyName, int javaVersion, params string[] buildServerTexts)
		{
			ServerName = serverName;
			ServerFriendlyName = serverFriendlyName;
			JavaVersion = javaVersion;
			BuildServerTexts = buildServerTexts.Union(new string[] { serverName, serverFriendlyName }.Distinct()).ToArray();
		}
		public MinecraftServerData(string serverName, int javaVersion, params string[] buildServerTexts) : this(serverName, serverName, javaVersion, buildServerTexts)
		{
		}

		public string ServerName { get; private set; }
		public string ServerFriendlyName { get; private set; }
		public string[] BuildServerTexts { get; private set; }
		public int JavaVersion { get; private set; }
	}
}
