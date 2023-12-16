const fs = require("fs")

function readSecret(secretName) {
  return fs.readFileSync("/run/secrets/" + secretName, "utf8").trim()
}

const db_name = process.env.MONGO_DATABASE
const password = readSecret("mongo-password")
const username = readSecret("mongo-username")

console.log("
Disable usage data collection.")
disableTelemetry()

try {
  db.createUser(
    {
      user: username,
      pwd: password,
      roles:
        [
          {role: "readWrite", db: "admin" },
          {role: "readWrite", db: db_name },
          {role: "dbOwner", db: "test_pyproject_starter"},
        ]
    }
  )
  console.log("
Adding user: " + username)
} catch(error) {
  console.log("
User already exists: " + username)
}
