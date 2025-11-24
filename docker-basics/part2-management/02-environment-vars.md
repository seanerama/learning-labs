# Lesson 2: Environment Variables

Configure containers dynamically using environment variables!

## 🎯 Objective

Learn how to pass configuration to containers using environment variables instead of hard-coding values. This is essential for deploying the same container across different environments (dev, staging, production).

## 📝 What You'll Learn

- Setting environment variables with `-e` flag
- Using `--env-file` for multiple variables
- Viewing environment variables in running containers
- Best practices for sensitive data
- Creating environment-aware applications

## 🚀 Steps

### Step 1: Basic Environment Variable

```bash
# Set a simple environment variable
docker run --rm -e MY_VAR="Hello World" alpine sh -c 'echo $MY_VAR'
```

Output:
```
Hello World
```

The `-e` flag sets `MY_VAR=Hello World` inside the container.

### Step 2: Multiple Environment Variables

```bash
# Set multiple variables
docker run --rm \
  -e APP_ENV=production \
  -e APP_DEBUG=false \
  -e APP_PORT=3000 \
  alpine sh -c 'echo "Env: $APP_ENV, Debug: $APP_DEBUG, Port: $APP_PORT"'
```

Output:
```
Env: production, Debug: false, Port: 3000
```

### Step 3: Real Example with PostgreSQL

```bash
# Run PostgreSQL with environment-based configuration
docker run -d \
  --name postgres-demo \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=myapp \
  -p 5432:5432 \
  postgres:alpine

# Check logs to see it initialized with our config
docker logs postgres-demo
```

You'll see PostgreSQL created the `myapp` database with user `admin`!

### Step 4: Viewing Environment Variables

```bash
# View all environment variables in running container
docker exec postgres-demo env

# Or filter for specific ones
docker exec postgres-demo env | grep POSTGRES
```

Output:
```
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret123
POSTGRES_DB=myapp
```

### Step 5: Using Environment Files

Create a file with environment variables:

```bash
# Create .env file
cat > app.env << EOF
APP_NAME=MyApplication
APP_VERSION=1.0.0
APP_ENV=production
APP_DEBUG=false
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=admin
EOF

# View the file
cat app.env
```

Now use it:

```bash
# Run container with --env-file
docker run --rm \
  --env-file app.env \
  alpine sh -c 'env | grep APP'
```

Output:
```
APP_NAME=MyApplication
APP_VERSION=1.0.0
APP_ENV=production
APP_DEBUG=false
```

### Step 6: Overriding Image Defaults

Many images have default environment variables you can override:

```bash
# MySQL has default user 'root', let's check defaults
docker run --rm mysql:8.0 env | grep MYSQL

# Run MySQL with custom configuration
docker run -d \
  --name mysql-demo \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=testdb \
  -e MYSQL_USER=appuser \
  -e MYSQL_PASSWORD=apppass \
  -p 3306:3306 \
  mysql:8.0

# Wait for startup
sleep 15

# Check it created our database and user
docker exec mysql-demo mysql -uappuser -papppass -e "SHOW DATABASES;"
```

### Step 7: Environment Variables in Application

Let's run a real application that uses environment variables:

```bash
# Run Redis with custom configuration via env vars
docker run -d \
  --name redis-demo \
  -e REDIS_PORT=6379 \
  -e REDIS_PASSWORD=mysecret \
  -p 6379:6379 \
  redis:alpine redis-server --requirepass mysecret

# Test connection (needs password)
docker exec redis-demo redis-cli -a mysecret PING
```

Output:
```
PONG
```

### Step 8: Inspect Environment Variables

```bash
# View env vars via docker inspect
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' postgres-demo

# Or get specific env var
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' postgres-demo | grep POSTGRES_USER
```

## 🧪 Practical Scenarios

### Scenario 1: Multi-Environment Deployment

Create different environment files:

```bash
# Development environment
cat > .env.dev << EOF
APP_ENV=development
APP_DEBUG=true
DB_HOST=dev-db.local
LOG_LEVEL=debug
EOF

# Production environment
cat > .env.prod << EOF
APP_ENV=production
APP_DEBUG=false
DB_HOST=prod-db.local
LOG_LEVEL=warning
EOF

# Run in dev
docker run --rm --env-file .env.dev alpine sh -c 'env | grep APP'

# Run in prod
docker run --rm --env-file .env.prod alpine sh -c 'env | grep APP'
```

### Scenario 2: Database Configuration

```bash
# Create database environment file
cat > db.env << EOF
POSTGRES_USER=dbadmin
POSTGRES_PASSWORD=secure_password_123
POSTGRES_DB=production_db
POSTGRES_INITDB_ARGS=--encoding=UTF-8
EOF

# Run PostgreSQL with file
docker run -d \
  --name prod-db \
  --env-file db.env \
  -v db-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine

# Verify configuration
docker exec prod-db psql -U dbadmin -d production_db -c '\l'
```

### Scenario 3: Application with Dependencies

```bash
# Full application stack environment
cat > stack.env << EOF
# App config
APP_NAME=WebApp
APP_PORT=3000
NODE_ENV=production

# Database config
DB_HOST=postgres
DB_PORT=5432
DB_NAME=webapp
DB_USER=webapp_user
DB_PASS=webapp_pass

# Redis config
REDIS_HOST=redis
REDIS_PORT=6379

# External API
API_KEY=your-api-key-here
API_URL=https://api.example.com
EOF

# Run app with all config
docker run -d \
  --name webapp \
  --env-file stack.env \
  -p 3000:3000 \
  node:alpine sh -c 'env && sleep infinity'

# Check configuration
docker exec webapp env | grep -E "APP_|DB_|REDIS_|API_"
```

### Scenario 4: Overriding Specific Variables

```bash
# Use env file but override specific values
docker run --rm \
  --env-file .env.prod \
  -e APP_DEBUG=true \
  -e LOG_LEVEL=debug \
  alpine sh -c 'env | grep -E "APP_|LOG_"'

# The -e flags override values from the file!
```

## 💡 Key Concepts

### Environment Variable Precedence

```
┌─────────────────────────────────────────────┐
│     Environment Variable Priority          │
│     (highest to lowest)                     │
├─────────────────────────────────────────────┤
│                                             │
│  1. -e flag (docker run -e VAR=value)      │
│  2. --env-file (docker run --env-file)     │
│  3. Dockerfile ENV (ENV VAR=value)         │
│  4. Container defaults                      │
│                                             │
└─────────────────────────────────────────────┘
```

### Environment File Format

```bash
# Comments are allowed
# KEY=VALUE format, no spaces around =

APP_NAME=MyApp          # ✅ Correct
APP_ENV=production      # ✅ Correct

# Quotes are optional but recommended for values with spaces
APP_TITLE="My Application"   # ✅ Correct
APP_TITLE=My Application      # ❌ Wrong - breaks on space

# No spaces around =
APP_PORT = 3000         # ❌ Wrong
APP_PORT=3000           # ✅ Correct

# Empty values are okay
OPTIONAL_VAR=           # ✅ Sets empty string

# No export keyword needed
export APP_VAR=value    # ❌ Wrong - this is bash syntax
APP_VAR=value           # ✅ Correct
```

### When to Use Environment Variables

**✅ GOOD uses:**
- Configuration that changes between environments (dev/staging/prod)
- Database credentials
- API keys and tokens
- Feature flags
- Port numbers
- Hostnames and URLs

**❌ AVOID for:**
- Large binary data
- Entire config files (use volumes instead)
- Secrets in production (use Docker secrets or vault)

## ✅ Practice Exercises

### Exercise 1: Configure Nginx

Configure Nginx using environment variables:

<details>
<summary>Solution</summary>

```bash
# Create environment file for Nginx
cat > nginx.env << EOF
NGINX_HOST=localhost
NGINX_PORT=80
EOF

# Note: Stock nginx doesn't use these directly,
# but custom nginx images often do

# Run with env vars (they're available in container)
docker run -d \
  --name nginx-env \
  --env-file nginx.env \
  -p 8080:80 \
  nginx:alpine

# Check env vars are set
docker exec nginx-env env | grep NGINX

# Clean up
docker rm -f nginx-env
```
</details>

### Exercise 2: Multi-Container with Shared Config

Run two containers with the same environment file:

<details>
<summary>Solution</summary>

```bash
# Create shared config
cat > shared.env << EOF
APP_VERSION=2.0.0
ENVIRONMENT=staging
LOG_LEVEL=info
EOF

# Run two containers with same config
docker run -d --name app1 --env-file shared.env alpine sleep infinity
docker run -d --name app2 --env-file shared.env alpine sleep infinity

# Verify both have same config
echo "=== App 1 ==="
docker exec app1 env | grep -E "APP_|ENVIRONMENT|LOG_"

echo "=== App 2 ==="
docker exec app2 env | grep -E "APP_|ENVIRONMENT|LOG_"

# Clean up
docker rm -f app1 app2
```
</details>

### Exercise 3: Environment-Specific Database

Create and run different database configs:

<details>
<summary>Solution</summary>

```bash
# Development database
cat > db-dev.env << EOF
POSTGRES_USER=dev
POSTGRES_PASSWORD=devpass
POSTGRES_DB=devdb
EOF

# Production database
cat > db-prod.env << EOF
POSTGRES_USER=produser
POSTGRES_PASSWORD=SuperSecure123!
POSTGRES_DB=productiondb
EOF

# Run dev database
docker run -d \
  --name dev-db \
  --env-file db-dev.env \
  -p 5433:5432 \
  postgres:alpine

# Run prod database
docker run -d \
  --name prod-db \
  --env-file db-prod.env \
  -p 5434:5432 \
  postgres:alpine

# Wait for startup
sleep 10

# Check dev config
docker exec dev-db psql -U dev -d devdb -c "SELECT current_database(), current_user;"

# Check prod config
docker exec prod-db psql -U produser -d productiondb -c "SELECT current_database(), current_user;"

# Clean up
docker rm -f dev-db prod-db
```
</details>

## 🔧 Advanced Usage

### Using Shell Variables in Docker Run

```bash
# Set shell variables
export DB_HOST=prod-server.local
export DB_PORT=5432

# Use them in docker run
docker run --rm \
  -e DB_HOST=$DB_HOST \
  -e DB_PORT=$DB_PORT \
  alpine sh -c 'echo "Connecting to $DB_HOST:$DB_PORT"'
```

### Dynamic Environment Files

```bash
# Generate environment file dynamically
cat > generate-env.sh << 'EOF'
#!/bin/bash
echo "APP_VERSION=$(git describe --tags)"
echo "BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "GIT_COMMIT=$(git rev-parse --short HEAD)"
EOF

chmod +x generate-env.sh

# Generate and use
./generate-env.sh > dynamic.env
docker run --rm --env-file dynamic.env alpine env | grep -E "APP_|BUILD_|GIT_"
```

### Environment Variable Substitution

```bash
# Create template
cat > config.env << 'EOF'
DB_HOST=database.local
DB_PORT=5432
# Use variables within the file
DB_URL=postgresql://${DB_HOST}:${DB_PORT}/mydb
EOF

# Docker doesn't do substitution, but your app might!
docker run --rm --env-file config.env alpine env
```

### Inspecting Environment from Host

```bash
# Get environment as JSON
docker inspect -f '{{json .Config.Env}}' my-container | jq

# Get specific env var value
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' my-container | \
  grep "^POSTGRES_USER=" | \
  cut -d= -f2
```

## 📊 Useful One-Liners

```bash
# List all env vars for running container
docker exec <container> env

# Find containers with specific env var
docker ps -q | xargs -I {} sh -c 'echo -n "{}: "; docker inspect -f "{{.Config.Env}}" {} | grep MY_VAR || echo "not found"'

# Export container's env to file
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' my-container > extracted.env

# Compare env vars between two containers
diff <(docker exec container1 env | sort) <(docker exec container2 env | sort)

# Show only custom env vars (filter out system defaults)
docker exec my-container env | grep -v -E "^(PATH|HOSTNAME|HOME|TERM)="
```

## ❓ Common Issues

### Issue: Environment variable not working

**Symptoms:** Variable is set but app doesn't see it

**Debug:**
```bash
# 1. Check if variable is actually set
docker exec my-container env | grep MY_VAR

# 2. Check if application is reading it correctly
docker exec my-container sh -c 'echo $MY_VAR'

# 3. Some applications need variables at build time, not runtime
# Check the application's documentation
```

### Issue: Quotes in environment file causing problems

**Problem:**
```bash
# In .env file
MY_VAR="value with spaces"
```

**Solution:**
```bash
# Docker handles quotes differently than bash
# Both of these work:
MY_VAR=value with spaces
MY_VAR="value with spaces"

# But this is wrong:
MY_VAR='value with spaces'  # Single quotes included in value!
```

### Issue: Cannot find environment file

**Error:** `open /path/to/.env: no such file or directory`

**Solution:**
```bash
# Use absolute path
docker run --env-file /absolute/path/to/.env my-image

# Or relative to current directory
docker run --env-file ./relative/path/.env my-image

# Check file exists
ls -la .env
```

### Issue: Environment variable with special characters

**Problem:**
```bash
PASSWORD=P@ssw0rd!  # May cause issues with special chars
```

**Solution:**
```bash
# Use quotes in the env file
PASSWORD="P@ssw0rd!"

# Or escape special characters
PASSWORD=P@ssw0rd\!
```

## 🎯 Best Practices

### 1. Use Environment Files for Multiple Variables

```bash
# ✅ GOOD - Clean and maintainable
docker run --env-file app.env my-app

# ❌ AVOID - Hard to read and maintain
docker run -e VAR1=a -e VAR2=b -e VAR3=c -e VAR4=d -e VAR5=e my-app
```

### 2. Never Commit Secrets to Git

```bash
# ✅ GOOD - Add to .gitignore
echo "*.env" >> .gitignore
echo ".env.*" >> .gitignore

# Commit template instead
cp .env .env.example
sed 's/=.*/=/' .env.example  # Remove values
git add .env.example
```

### 3. Use Descriptive Variable Names

```bash
# ✅ GOOD - Clear and specific
DB_HOST=postgres
DB_PORT=5432
DB_NAME=myapp

# ❌ AVOID - Ambiguous
HOST=postgres
PORT=5432
NAME=myapp
```

### 4. Document Required Variables

```bash
# Create .env.example with descriptions
cat > .env.example << EOF
# Database Configuration
DB_HOST=localhost          # Database server hostname
DB_PORT=5432              # Database server port
DB_NAME=myapp             # Database name
DB_USER=admin             # Database username
DB_PASS=                  # Database password (required)

# Application Configuration
APP_ENV=development       # Environment: development, staging, production
APP_DEBUG=true            # Enable debug mode (true/false)
EOF
```

### 5. Validate Required Variables

```bash
# Check required variables before starting
docker run --rm --env-file .env alpine sh -c '
  if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ]; then
    echo "Error: DB_HOST and DB_PORT are required"
    exit 1
  fi
  echo "Configuration valid"
'
```

## 🔐 Security Considerations

### Viewing Environment Variables is Easy

```bash
# Anyone with Docker access can see env vars
docker exec my-container env
docker inspect my-container

# Better for secrets: Use Docker secrets (Swarm) or vault
```

### Environment Variables in Logs

```bash
# ⚠️ WARNING: Env vars can leak in logs
docker run alpine sh -c 'echo "Password: $PASSWORD"'  # BAD!

# ✅ BETTER: Don't log sensitive data
docker run alpine sh -c 'echo "Authentication configured"'
```

### Alternative for Sensitive Data

Preview for production:
```bash
# Use Docker secrets (requires Swarm mode)
echo "my-secret-password" | docker secret create db_password -

# Or mount secrets as files
docker run -v /secure/secrets:/secrets:ro my-app
# App reads from /secrets/db_password instead of env var
```

## 🎉 Lesson Complete!

You now know:

✅ How to set environment variables with `-e`
✅ How to use environment files with `--env-file`
✅ How to view and inspect environment variables
✅ Best practices for different environments
✅ Security considerations for sensitive data

### What's Next?

**Next Lesson:** [03 - Volumes →](03-volumes.md)

Learn how to persist data beyond container lifecycle with volumes!

---

**Lesson Duration:** 20 minutes
**Difficulty:** Beginner
**Prerequisites:** Lesson 1 completed
**Skills:** Configuration management, environment separation
