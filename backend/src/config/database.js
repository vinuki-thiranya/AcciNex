const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://admin:securepassword123@localhost:5432/accinex',
});

module.exports = {
  query: (text, params) => pool.query(text, params),
};
