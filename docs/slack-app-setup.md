# Slack App Setup Guide

This guide walks you through setting up your Slack app to work with Slacktable.

## Prerequisites

- A Slack workspace where you have permission to install apps
- Admin access to create and configure Slack apps

## Step 1: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter the following details:
   - **App Name**: `Slacktable`
   - **Development Slack Workspace**: Choose your workspace
5. Click **"Create App"**

## Step 2: Configure Basic Information

1. In your app's **Basic Information** page, note down:
   - **App ID** (you'll need this for reference)
   - **Signing Secret** (under App Credentials)

## Step 3: Set Up Bot Token Scopes

1. Navigate to **OAuth & Permissions** in the left sidebar
2. Scroll down to **Scopes** section
3. Under **Bot Token Scopes**, add the following scopes:
   - `channels:history` - Read messages in public channels
   - `groups:history` - Read messages in private channels
   - `im:history` - Read messages in direct messages
   - `mpim:history` - Read messages in group direct messages
   - `reactions:read` - Read emoji reactions
   - `users:read` - Read user information
   - `channels:read` - Read channel information

## Step 4: Install the App to Your Workspace

1. Still in **OAuth & Permissions**, scroll up to the top
2. Click **"Install to Workspace"**
3. Review the permissions and click **"Allow"**
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

## Step 5: Configure Event Subscriptions

1. Navigate to **Event Subscriptions** in the left sidebar
2. Turn on **Enable Events**
3. In the **Request URL** field, enter your deployed app URL:
   ```
   https://your-app-domain.vercel.app/slack/events
   ```
   - Replace `your-app-domain` with your actual Vercel deployment URL
   - Slack will verify this URL, so make sure your app is deployed first

4. Under **Subscribe to bot events**, add:
   - `reaction_added`
   - `reaction_removed`

5. Click **"Save Changes"**

## Step 6: Configure App-Level Tokens (Optional)

If you want to use Socket Mode for real-time events:

1. Navigate to **Basic Information**
2. Scroll down to **App-Level Tokens**
3. Click **"Generate Token and Scopes"**
4. Enter a name like `socket-mode-token`
5. Add the scope `connections:write`
6. Click **"Generate"**
7. Copy the token (starts with `xapp-`)

## Step 7: Install the App in Channels

1. Go to any Slack channel where you want to use the app
2. Type `/invite @Slacktable` to invite the bot
3. The bot will appear in the channel members

## Step 8: Set Environment Variables

In your deployment environment (Vercel), set these environment variables:

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token (if using Socket Mode)
```

## Step 9: Test the Installation

1. Send a test message in a channel where the bot is installed
2. React to the message with the `:fedex:` emoji
3. Check your Airtable base to see if the record was created
4. Monitor your app logs for any errors

## Troubleshooting

### Common Issues

1. **Events not being received**
   - Verify your Request URL is correct and accessible
   - Check that the bot is installed in the channel where you're testing
   - Ensure proper bot token scopes are set

2. **Permission errors**
   - Make sure the bot has the required scopes
   - Verify the bot is invited to the channel

3. **URL verification fails**
   - Ensure your app is deployed and accessible
   - Check that the `/slack/events` endpoint is working

### Useful Commands

- Test bot permissions: `curl -H "Authorization: Bearer xoxb-your-token" https://slack.com/api/auth.test`
- Check bot info: `curl -H "Authorization: Bearer xoxb-your-token" https://slack.com/api/users.info?user=BOT_USER_ID`

## Security Notes

- Never commit tokens to version control
- Use environment variables for all sensitive information
- Regularly rotate your tokens
- Monitor your app's usage and logs

---

**Next Steps**: After completing this setup, proceed to [Airtable Setup](airtable-setup.md) to configure your Airtable integration.
