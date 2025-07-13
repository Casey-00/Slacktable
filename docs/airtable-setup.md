# Airtable Setup Guide

This guide walks you through setting up your Airtable base and API access for Slacktable.

## Prerequisites

- An Airtable account (free tier is sufficient)
- Access to create and modify bases

## Step 1: Create or Access Your Airtable Base

### If you already have a base:
1. Navigate to your existing base
2. Ensure it has a table named **"Bugs"** (case-sensitive)
3. Ensure the table has a field named **"Name"** (case-sensitive)

### If you need to create a new base:
1. Go to [airtable.com](https://airtable.com)
2. Sign in to your account
3. Click **"Create a base"**
4. Choose **"Start from scratch"**
5. Name your base (e.g., "Bug Tracking")

## Step 2: Set Up Your Table Structure

1. In your base, create or rename a table to **"Bugs"**
2. Ensure the table has a field named **"Name"** of type **"Single line text"**
3. You can add additional fields if needed:
   - **"Description"** (Long text)
   - **"Priority"** (Single select: Low, Medium, High)
   - **"Status"** (Single select: Open, In Progress, Closed)
   - **"Created"** (Date)
   - **"Assigned to"** (Single select or User field)

## Step 3: Get Your Base ID

1. Go to [airtable.com/api](https://airtable.com/api)
2. Click on your base
3. In the introduction section, you'll see something like:
   ```
   The ID of this base is app8JlYvQ0jwjT5dD
   ```
4. Copy this Base ID (it starts with `app`)

**Note**: Your Base ID is already configured in the app as `app8JlYvQ0jwjT5dD`. If your base has a different ID, you'll need to update the environment variable.

## Step 4: Create an API Token

1. Go to [airtable.com/create/tokens](https://airtable.com/create/tokens)
2. Click **"Create new token"**
3. Give your token a name (e.g., "Slacktable Integration")
4. Set the scopes:
   - **data.records:read** - Read records
   - **data.records:write** - Create records
   - **schema.bases:read** - Read base schema
5. Select access to your specific base
6. Click **"Create token"**
7. Copy the token (it starts with `pat`) and store it securely

## Step 5: Test Your Setup

You can test your Airtable configuration using curl:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.airtable.com/v0/YOUR_BASE_ID/Bugs
```

Replace:
- `YOUR_TOKEN` with your Personal Access Token
- `YOUR_BASE_ID` with your Base ID

## Step 6: Set Environment Variables

In your deployment environment (Vercel), set these environment variables:

```env
AIRTABLE_API_TOKEN=pat-your-personal-access-token
AIRTABLE_BASE_ID=app8JlYvQ0jwjT5dD
AIRTABLE_TABLE_NAME=Bugs
AIRTABLE_FIELD_NAME=Name
```

## Step 7: Verify the Integration

1. Deploy your app with the Airtable configuration
2. Test by reacting to a Slack message with `:fedex:`
3. Check your Airtable base to see if a new record was created
4. The message text should appear in the "Name" field

## Customization Options

### Different Field Name
If you want to use a different field name:
1. Update the `AIRTABLE_FIELD_NAME` environment variable
2. Ensure the field exists in your table

### Different Table Name
If you want to use a different table name:
1. Update the `AIRTABLE_TABLE_NAME` environment variable
2. Ensure the table exists in your base

### Multiple Fields
To write to multiple fields, you can modify the `create_airtable_record` function in `app/slack/handlers.py`:

```python
fields = {
    settings.airtable_field_name: message_text,
    "Status": "Open",
    "Created": datetime.now().isoformat(),
    "Priority": "Medium"
}
```

## Troubleshooting

### Common Issues

1. **"Table not found" error**
   - Verify table name is exactly "Bugs" (case-sensitive)
   - Check that the base ID is correct

2. **"Field not found" error**
   - Verify field name is exactly "Name" (case-sensitive)
   - Ensure the field exists in your table

3. **Permission errors**
   - Verify your API token has the correct scopes
   - Check that the token has access to the specific base

4. **API rate limits**
   - Airtable has rate limits (5 requests per second)
   - The app handles basic rate limiting, but high usage may require additional handling

### Useful Commands

Test your API token:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.airtable.com/v0/meta/bases
```

Get base schema:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.airtable.com/v0/meta/bases/YOUR_BASE_ID/tables
```

## Security Notes

- Never commit API tokens to version control
- Use environment variables for all sensitive information
- Regularly rotate your API tokens
- Monitor your API usage in Airtable

## Data Management

### Viewing Records
- Records created by Slacktable will appear in your Airtable base
- You can view, edit, and organize them using Airtable's interface

### Backup
- Consider regular backups of your Airtable data
- Airtable provides export functionality for this purpose

### Cleanup
- Implement a regular cleanup process for old records if needed
- Consider archiving rather than deleting for audit purposes

---

**Next Steps**: After completing this setup, proceed to [Deployment Guide](deployment.md) to deploy your app to Vercel.
