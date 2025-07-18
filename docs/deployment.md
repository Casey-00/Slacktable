# Deployment Guide

Deploy your Slacktable app to Fly.io using Socket Mode for reliable, persistent connections to Slack.

## Prerequisites

- Fly.io account ([Sign up here](https://fly.io/app/sign-up))
- Fly.io CLI installed ([Installation guide](https://fly.io/docs/hands-on/install-flyctl/))
- Docker installed on your local machine

## Step 1: Prepare Your Project

1. Ensure your project has the required files:
   - `requirements.txt`: Lists all Python dependencies
   - `run_socket_mode.py`: Main application entry point
   - `.env.example`: Template for environment variables

## Step 2: Create Fly.io Configuration

1. Initialize your Fly.io app:
   ```bash
   flyctl auth login
   flyctl launch
   ```
   Follow the prompts to create a new app. Choose a unique name and select a region.

2. This will create a `fly.toml` configuration file. Update it as needed for Python deployment.

## Step 3: Set Up Environment Variables

1. Set your environment variables using Fly.io secrets:
   ```bash
   flyctl secrets set SLACK_BOT_TOKEN=your_bot_token_here
   flyctl secrets set SLACK_APP_TOKEN=your_app_token_here
   flyctl secrets set AIRTABLE_API_TOKEN=your_airtable_token_here
   flyctl secrets set AIRTABLE_BASE_ID=your_base_id_here
   flyctl secrets set AIRTABLE_TABLE_NAME=your_table_name_here
   flyctl secrets set AIRTABLE_FIELD_NAME=your_field_name_here
   flyctl secrets set TARGET_EMOJI=fedex
   ```

   **Note**: The `SLACK_SIGNING_SECRET` is not needed for Socket Mode.

## Step 4: Create Dockerfile

Create a `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run_socket_mode.py"]
```

## Step 5: Deploy to Fly.io

1. Deploy your application:
   ```bash
   flyctl deploy
   ```

2. Monitor the deployment logs:
   ```bash
   flyctl logs
   ```

## Step 6: Verify the Deployment

1. Check your app status:
   ```bash
   flyctl status
   ```

2. Monitor logs to ensure the Socket Mode connection is established:
   ```bash
   flyctl logs -a your-app-name
   ```
   Look for messages indicating successful connection to Slack.

## Step 7: Test the Slack Integration

1. React to a message in Slack with the `:fedex:` emoji (or your configured emoji).
2. Confirm a new record appears in your Airtable table.
3. Monitor logs in Fly.io for any errors:
   ```bash
   flyctl logs -a your-app-name
   ```

## Troubleshooting

### Deployment Issues

1. **Build/Compile Errors**
   - Check `requirements.txt` for any missing dependencies.
   - Ensure your Dockerfile is properly configured.

2. **Environment Variables Not Set**
   - Verify secrets are set: `flyctl secrets list`
   - Check that variable names match your code exactly.

3. **App Not Starting**
   - Check logs: `flyctl logs`
   - Ensure `run_socket_mode.py` is executable and imports work correctly.

### Slack Connection Issues

1. **Socket Mode Not Connecting**
   - Verify `SLACK_APP_TOKEN` has `connections:write` scope.
   - Check that Socket Mode is enabled in your Slack app settings.
   - Ensure the bot is installed in your workspace.

2. **Events Not Received**
   - Verify your Slack app has the required OAuth scopes:
     - `reactions:read`
     - `channels:history`
   - Ensure the bot is added to the channels where you're testing.

### Airtable Integration Issues

1. **Records Not Created**
   - Verify `AIRTABLE_API_TOKEN` has write permissions.
   - Check that `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_NAME`, and `AIRTABLE_FIELD_NAME` are correct.
   - Monitor logs for Airtable API errors.

## Scaling and Monitoring

- **Scaling**: Fly.io apps auto-scale based on demand. For consistent performance, consider setting a minimum number of instances.
- **Monitoring**: Use `flyctl logs` and `flyctl metrics` to monitor your app's performance.
- **Alerts**: Set up monitoring and alerts through Fly.io dashboard for production deployments.

## Security Notes

- Rotate your tokens regularly.
- Monitor your application's usage and logs.
- Use Fly.io secrets for all sensitive environment variables.
- Consider setting up log forwarding for production monitoring.

## Conclusion

Your Slacktable app is now deployed on Fly.io with Socket Mode, providing reliable real-time processing of Slack emoji reactions. The persistent connection ensures no events are missed!

For additional support, visit Fly.io's [documentation](https://fly.io/docs/) or Slack's [Socket Mode docs](https://api.slack.com/apis/connections/socket).

---

If you encounter issues or have questions, feel free to create an issue in the [GitHub repository](https://github.com/Casey-00/Slacktable).

