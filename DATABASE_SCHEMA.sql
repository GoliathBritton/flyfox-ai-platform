-- CUSTOMERS TABLE

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    company TEXT,
    phone TEXT,
    subscription_tier TEXT DEFAULT 'starter',
    subscription_status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    stripe_customer_id TEXT,
    paypal_customer_id TEXT,
    api_calls_used INTEGER DEFAULT 0,
    api_calls_limit INTEGER DEFAULT 5
);

-- PAYMENTS TABLE

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    amount DECIMAL(10,2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    payment_method TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    stripe_payment_id TEXT,
    paypal_payment_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

-- API_USAGE TABLE

CREATE TABLE IF NOT EXISTS api_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    endpoint TEXT NOT NULL,
    response_time INTEGER,
    success BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

-- QUANTUM_JOBS TABLE

CREATE TABLE IF NOT EXISTS quantum_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    job_type TEXT NOT NULL,
    provider TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    result_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

