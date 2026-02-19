import fs from 'fs'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const USERS_FILE = join(__dirname, 'data', 'users.json')

// Ensure data directory exists
function ensureDataDir() {
  const dataDir = join(__dirname, 'data')
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true })
  }
}

// Load users from file
export function loadUsers() {
  ensureDataDir()
  try {
    if (fs.existsSync(USERS_FILE)) {
      const data = fs.readFileSync(USERS_FILE, 'utf-8')
      return JSON.parse(data)
    }
  } catch (error) {
    console.error('Error loading users:', error.message)
  }
  return {}
}

// Save users to file
export function saveUsers(users) {
  ensureDataDir()
  try {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2))
    return true
  } catch (error) {
    console.error('Error saving users:', error.message)
    return false
  }
}

// Hash password (simple implementation - use bcrypt in production)
export function hashPassword(password) {
  return Buffer.from(password).toString('base64')
}

// Verify password
export function verifyPassword(password, hash) {
  return hashPassword(password) === hash
}

// Get user by username
export function getUserByUsername(username, users) {
  return users[username] || null
}

// Create new user
export function createUser(username, userObj, users) {
  users[username] = {
    ...userObj,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  }
  return saveUsers(users)
}

// Update user
export function updateUser(username, updates, users) {
  if (users[username]) {
    users[username] = {
      ...users[username],
      ...updates,
      updatedAt: new Date().toISOString(),
    }
    return saveUsers(users)
  }
  return false
}
