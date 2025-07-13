# Deployment Guide

Deploy your Slacktable app to Vercel for a seamless and scalable hosting solution.

## Prerequisites

- Vercel account ([Sign up here](https://vercel.com/signup))
- Vercel CLI installed (`npm install -g vercel`)

## Step 1: Prepare Your Project

1. Ensure your project has the required file structure and files:
   - `vercel.json`: Contains project configuration for Vercel
   - `requirements.txt`: Lists all Python dependencies

## Step 2: Set Up Vercel CLI

1. Authenticate your Vercel CLI:
   ```bash
   vercel login
   ```
   Follow the on-screen instructions to log in.

2. Link your project:
   ```bash
   vercel link
   ```
   Follow the prompts to associate your local project with a Vercel project.

## Step 3: Deploy to Vercel

1. Deploy your application:
   ```bash
   vercel --prod
   ```
   This will create a production deployment.

2. If you need a preview deployment, simply run:
   ```bash
   vercel
   ```

3. Follow the on-screen instructions and note the deployment URL.

## Step 4: Configure Environment Variables

1. Navigate to the Vercel dashboard in your browser.
2. Go to your project settings.
3. Click on **Environment Variables**.
4. Add the following variables from your local `.env` configuration:
   - `SLACK_BOT_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `SLACK_APP_TOKEN` (if using Socket Mode)
   - `AIRTABLE_API_TOKEN`
   - `AIRTABLE_BASE_ID`
   - `AIRTABLE_TABLE_NAME`
   - `AIRTABLE_FIELD_NAME`
   - `TARGET_EMOJI`

5. Save the changes.

## Step 5: Verify the Deployment

1. Visit your application URL (e.g., `https://your-app-domain.vercel.app`).
2. Check `/health` endpoint to ensure the app is running:
   ```
   https://your-app-domain.vercel.app/health
   ```
   You should see a JSON response with "status": "healthy".

## Step 6: Test the Slack Integration

1. React to a message in Slack with the `:fedex:` emoji.
2. Confirm a new record appears in your Airtable "Bugs" table.
3. Monitor logs in Vercel dashboard for any errors.

## Troubleshooting

### Deployment Issues

1. **Build/Compile Errors**
   - Check `requirements.txt` for any missing dependencies.
   - Ensure your Python version locally matches the Vercel environment.

2. **Environment Variables Not Set**
   - Double-check environment variables in the Vercel dashboard.

3. **App Not Starting**
   - Check your `vercel.json` for correct path configuration.
   - Validate FastAPI app entry point (`app/main.py`).

### Slack Event Issues

1. **Events Not Received**
   - Ensure Slack app installed with proper permissions.
   - Verify the correct event subscription URL in Slack.

## Security Notes

- Rotate your tokens regularly.
- Monitor your application's usage.
- Set up alerts for unexpected errors or usage spikes.

## Conclusion

Your app is now live on Vercel and ready to start processing Slack messages with the `:fedex:` emoji. Enjoy tracking bugs and feedback effortlessly!

For additional support, visit Vercel's [documentation](https://vercel.com/docs) or Slack's [API docs](https://api.slack.com/docs).

---

If you've encountered issues or have questions, feel free to reach out for support or consider creating an issue in the [GitHub repository](https://github.com/Casey-00/Slacktable).

