#!/bin/bash

# SSH into your server and run the database initialization script
ssh -o StrictHostKeyChecking=no $USERNAME@$HOST << 'EOF'
    cd ~/fastapi_app
    source venv/bin/activate
    echo "Running database initialization script..."
    python -m app.db_init
    echo "Done initializing database."
EOF
