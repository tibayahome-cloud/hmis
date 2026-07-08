# Whachanga

Whachanga is a simple web app that acts as a WhatsApp treasurer assistant for group fund drives in Kenya. It makes it easy for WhatsApp group members to contribute using mobile money (MPESA / Airtel Money), tracks contributions and withdrawals, and notifies the group via a WhatsApp bot.

Live demo: https://whachanga.vercel.app

## Quick overview

- Admin adds the Whachanga bot to a WhatsApp group by pasting the invite link into the Register form.
- The backend uses the WhatsApp API to join the group and saves group metadata (group id, owner phone and encrypted withdraw pin) to the database.
- The bot announces the group and a contribution link for members.
- Members open the contribution link, fill a small form (name, phone, amount) and an STK push (MPESA/Airtel Money) is sent to the payer.
- On successful payment the backend records the payment and the bot posts a thank-you message and an updated table of contributors into the group.
- Admins can request withdrawals via WhatsApp by sending `WITHDRAW`. The bot replies with a list of owned groups and withdraw links. Withdraw flow requires the admin to enter recipient details and the withdraw pin; an OTP is sent to the admin's WhatsApp number to confirm the withdraw.

## Key features

- WhatsApp bot for group onboarding and notifications
- Contribution page with STK push payment integration
- Automatic recording of successful payments
- Withdraw flow protected by 4-digit pin + OTP sent via WhatsApp
- Simple ASCII contribution table posted to group on each update
- Fees: contribution payers cover transaction cost (~2.5%). Admins pay withdraw network fees (MPESA charges).

## Architecture

- Frontend: Static pages served from the Flask app + simple HTML forms (deployed to Vercel)
- Backend: Flask app that handles web routes, interacts with the DB, Paystack (or MPESA gateway), and WhatsApp API
- Database: PostgreSQL (DATABASE_URL)
- External services:
	- WhatsApp API provider (WAHA or similar) for adding the bot to groups and sending messages
	- Paystack or an MPESA/Airtel gateway for STK push and transfers

## Repo layout

```
app.py                 # Flask application and route handlers
utils/                 # helper modules (db, paystack, waapi, helper functions)
static/                # CSS and client static assets
templates/             # HTML templates
requirements.txt       # Python dependencies
README.md              # This file
```

## Environment variables

Create a `.env` file in the project root or set these in your environment. Example `.env`:

```
# Database
DATABASE_URL=postgres://user:pass@localhost:5432/whachanga

# WhatsApp API (WAHA or provider)
WAHA_API_KEY=your_waha_api_key
WAHA_BASE_URL=https://api.waha.example

# Payment gateway (Paystack or MPESA gateway)
PAYSTACK_SECRET_KEY=sk_test_xxx
PAYSTACK_BASE_URL=https://api.paystack.co

# Optional: application settings
FLASK_ENV=development
SECRET_KEY=change-me
```

Notes:
- `DATABASE_URL` is mandatory. The app will raise an error if not set.
- Keep secrets out of source control.

## Local development

1. Create a Python virtual environment and activate it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a local Postgres database and set `DATABASE_URL` in `.env`.

3. Start the Flask app (development mode)

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

4. Visit `http://localhost:5000` and use the Register page to add a WhatsApp group (requires a working WhatsApp API credentials).

## Deployment (Vercel)

This project is configured for Vercel (see `vercel.json`). To deploy:

1. Push your repository to GitHub.
2. Create a new project in Vercel and point it to the repo.
3. In Vercel dashboard add the environment variables listed above.
4. Deploy. Vercel will build static assets and deploy the Flask app as an API (or use serverless functions depending on configuration).

Notes about Vercel: Vercel's serverless environment may have short-lived instances. If you rely on long-lived DB connections, prefer connection pooling or reconnect logic (the app includes a simple reconnect helper in `utils/db.py`).

## Security notes

- Withdraw PINs are stored encrypted (one-way or symmetric depending on implementation) — ensure proper key management.
- Use HTTPS everywhere (Vercel provides TLS). Do not expose secret keys in client-side code.
- Rate-limit actions that trigger STK pushes to avoid abuse.

## How the flows look (messages)

Bot welcome message posted to group on successful onboarding:

```
Dear Members,
Welcome to the group - Southside Shelter Funds Drive
I am an automated Whatsapp Treasurer Assistant, I will be ensuring that your contributions are secure,
automated and updated in real-time.
To contribute kindly click below link
https://whachanga.vercel.app/contribute/{group_id}
```

Bot thank-you message on successful payment (example):

```
Thank you Alice,
Your Contribution of KSh. 500 has been received by the Group - Suncity Builders.
Thank you for your support. May The Almighty God bless you abundantly.
```

Whatsapp Group Update
```
Dear Members,
Welcome to the group.
I am an automated Whatsapp Treasurer Assistant, I will be ensuring that your contributions are secure, automated and updated in real-time.
To contribute kindly click below link...
https://whachanga.vercel.app/contribute/{group_id}


✅ UPDATED CONTRIBUTION LIST ✅
+-----+--------------+--------+
| No. | NAME         | AMOUNT |
+-----+--------------+--------+
| 1   | John Doe     | 100    |
+-----+--------------+--------+
| 2   | Alice        | 500    |
+-----+--------------+--------+
| 3   | Jane         | 1,000  |
+-----+--------------+--------+
|     | TOTAL        | 1,600  |
+-----+--------------+--------+
|     | WITHDRAWALS  | 1,000  |
+-----+-------------+--------+
|     | BALANCE      | 600    |
+-----+-------------+--------+
```

Bot posts full updated contribution table after each payment (ASCII table) so group members can see current totals.

## Admin withdraw flow

1. Admin sends `WITHDRAW` to the bot's WhatsApp number.
2. Bot replies with a list of groups the admin owns and withdraw links.
3. Admin clicks the withdraw link: `https://whachanga.vercel.app/withdraw/{group_id}`.
4. Admin enters recipient name, phone, amount and the 4-digit withdraw PIN.
5. If the PIN matches, system sends an OTP to the admin's WhatsApp.
6. Admin enters the OTP on the frontend. On success the backend initiates the transfer and notifies the group.

## Troubleshooting

- Database connection errors: confirm `DATABASE_URL`, ensure DB is reachable and migrations (if any) have been applied.
- WhatsApp API errors: check `WAHA_API_KEY` and provider docs.
- Payment failures: review gateway logs and ensure correct callback/webhook URLs are configured.

## Contributing

Patches, bug reports and improvements are welcome. Open an issue or send a pull request.

## License

This project is MIT licensed (see `LICENSE`).