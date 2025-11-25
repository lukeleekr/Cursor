# Vibe Book

A collection of web development projects including React applications, vanilla HTML/CSS/JS projects, and learning exercises.

## 📁 Project Structure

- **Chapter 4/**
  - `instagram-app/` - Instagram clone built with Vite + React
  - `memo-app/` - Memo app built with Create React App
  - `hello.py` - Simple Python script
- **cursorstudy/** - Vanilla HTML/CSS/JS projects
- **naver-redesign/** - Naver redesign project
- **assets/** - Images and data files for various projects

## 🐳 Development Container Setup

This repository includes a **DevContainer** configuration that provides a unified development environment that works identically on:
- Windows desktop
- macOS (MacBook Pro)
- GitHub Codespaces
- VS Code Dev Containers
- Cursor / Antigravity

### Why Use DevContainer?

- **Consistent Environment**: Same tools and versions across all platforms
- **No Local Installation**: No need to install Node.js, Python, or other tools on your host machine
- **OS-Agnostic**: Works the same on Windows, macOS, and Linux
- **Easy Onboarding**: New team members can start coding immediately

### Prerequisites

- **Docker Desktop** installed and running
  - [Download for Windows](https://www.docker.com/products/docker-desktop/)
  - [Download for macOS](https://www.docker.com/products/docker-desktop/)
- **VS Code** or **Cursor** with Dev Containers extension installed

### Getting Started

#### Option 1: VS Code / Cursor on Windows or macOS

1. **Open the repository** in VS Code or Cursor
2. **Open Command Palette** (`Ctrl+Shift+P` on Windows/Linux, `Cmd+Shift+P` on macOS)
3. **Select**: `Dev Containers: Reopen in Container`
4. Wait for the container to build (first time may take a few minutes)
5. The container will automatically install all dependencies

#### Option 2: GitHub Codespaces

1. Go to your repository on GitHub
2. Click the **"Code"** button
3. Select **"Codespaces"** tab
4. Click **"Create codespace on main"**
5. Wait for the environment to initialize

### What's Included in the Container

- **Node.js 20 LTS** with npm
- **Python 3.11+** with pip
- **Git**, curl, wget, and common CLI tools
- **VS Code extensions**: ESLint, Prettier, Python

### Port Forwarding

The following ports are automatically forwarded:
- **3000** - Create React App development server (memo-app)
- **5173** - Vite development server (instagram-app)
- **8000** - Python server (if needed)

### Running Projects Inside the Container

Once the container is running, open a terminal and run:

#### Instagram App (Vite)
```bash
cd "Chapter 4/instagram-app"
npm run dev
```
The app will be available at `http://localhost:5173`

#### Memo App (Create React App)
```bash
cd "Chapter 4/memo-app"
npm start
```
The app will be available at `http://localhost:3000`

#### Python Script
```bash
cd "Chapter 4"
python3 hello.py
```

### Troubleshooting

#### Container won't start
- Make sure Docker Desktop is running
- Check Docker Desktop logs for errors
- Try rebuilding: `Dev Containers: Rebuild Container`

#### Port already in use
- Stop any local servers running on ports 3000, 5173, or 8000
- Or change the port in the project's configuration

#### Dependencies not installed
- Run manually: `bash .devcontainer/post-create.sh`
- Or reinstall: `cd "Chapter 4/instagram-app" && npm install`

### Manual Setup (Without DevContainer)

If you prefer to run locally without Docker:

1. **Install Node.js 20 LTS** from [nodejs.org](https://nodejs.org/)
2. **Install Python 3.11+** from [python.org](https://www.python.org/)
3. **Install dependencies**:
   ```bash
   cd "Chapter 4/instagram-app" && npm install
   cd "../memo-app" && npm install
   ```

## 🛠️ Tech Stack

- **React 19.2.0** - UI library
- **Vite** - Build tool for instagram-app
- **Create React App** - Build tool for memo-app
- **Python 3.11+** - For Python scripts
- **Vanilla HTML/CSS/JS** - For learning projects

## 📝 Notes

- All paths in the container are Linux-based (works identically on Windows, macOS, and Codespaces)
- The container uses the `node` user (non-root) for security
- Dependencies are automatically installed when the container is created
- Changes to code are persisted in your workspace folder

## 🤝 Contributing

1. Open the repository in a DevContainer
2. Make your changes
3. Test your changes
4. Commit and push

---

**Happy Coding! 🚀**

