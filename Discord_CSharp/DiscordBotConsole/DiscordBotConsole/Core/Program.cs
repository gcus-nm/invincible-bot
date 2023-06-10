﻿using Discord;
using Discord.Commands;
using Discord.WebSocket;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Reflection;
using System.Threading.Tasks;

namespace DiscordBotConsole.Core
{
	class Program
	{
		private const string BOT_TOKEN = "MTExNjgyMDg0NjY3ODM4MDYxNA.GrWmIL.9OXYLzlQW6eo7qAQartTu-ZVHUi0zyBO8Lwpi0";
		private const ulong BOT_CLIENT_ID = 1116820846678380614;

		public static DiscordSocketClient BotClient { get; private set; }
		public static CommandService BotCommandService { get; private set; }
		public static ServiceProvider BotServices { get; private set; }

		public static IMessageChannel ResentMessageChannel { get; private set; }

		private static void Main(string[] args) => new Program().MainAsync().GetAwaiter().GetResult();

		public async Task MainAsync()
		{
			var config = new DiscordSocketConfig
			{
				GatewayIntents = GatewayIntents.AllUnprivileged | GatewayIntents.MessageContent
			};

			BotClient = new DiscordSocketClient(config);
			BotCommandService = new CommandService();
			BotServices = new ServiceCollection().BuildServiceProvider();

			BotClient.MessageReceived += OnRecievedMessage;

			await BotCommandService.AddModulesAsync(Assembly.GetEntryAssembly(), BotServices);
			await BotClient.LoginAsync(TokenType.Bot, BOT_TOKEN);
			await BotClient.StartAsync();

			await Task.Delay(-1);
		}

		private static async Task OnRecievedMessage(SocketMessage message)
		{
			var userMessage = message as SocketUserMessage;

			await MessageToCommand(userMessage);
		}

		private static async Task MessageToCommand(SocketUserMessage userMessage)
		{
			if (!BotUtility.IsValidMessage(userMessage))
			{
				return;
			}

			int index = 0;

			if (!(userMessage.HasCharPrefix('#', ref index) || userMessage.HasMentionPrefix(BotClient.CurrentUser, ref index)))
			{
				return;
			}

			var context = new CommandContext(BotClient, userMessage);
			var command = await BotCommandService.ExecuteAsync(context, index, BotServices);

			ResentMessageChannel = context.Channel;

			if (!command.IsSuccess)
			{
				await context.Channel.SendMessageAsync(command.ErrorReason);
			}
		}
	}
}
