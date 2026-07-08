
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
  id TEXT PRIMARY KEY,
  owner_phone TEXT NOT NULL,
  pin TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);


DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
  id TEXT PRIMARY KEY,
  group_id TEXT NOT NULL,
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  amount INT NOT NULL,
  type TEXT NOT NULL,
  checkout_request_id TEXT,
  status TEXT DEFAULT 'pending',
  confirmation_code TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
