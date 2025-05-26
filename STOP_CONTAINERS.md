# Stop Docker Containers Guide

This guide helps you stop any running Docker containers that might interfere with the Agent Angus LangChain deployment.

## 🛑 Quick Stop Commands

### Stop All Running Containers
```bash
# Stop all running containers
docker stop $(docker ps -q)

# Or if you prefer a more explicit approach
docker ps
docker stop <container_id_1> <container_id_2> ...
```

### Stop Specific Agent Angus Containers
```bash
# List running containers to identify Agent Angus related ones
docker ps

# Stop containers by name (if they have specific names)
docker stop angus-coordinator
docker stop angus-youtube
docker stop angus-database
docker stop angus-ai
docker stop coral-server

# Stop containers by image name pattern
docker ps --filter "ancestor=angus" -q | xargs docker stop
```

### Stop Docker Compose Services
If you were running Agent Angus with Docker Compose:

```bash
# Navigate to the directory with docker-compose.yml
cd /path/to/your/docker-compose/directory

# Stop all services
docker-compose down

# Stop and remove volumes (if you want to clean up completely)
docker-compose down -v

# Stop and remove everything including images
docker-compose down --rmi all -v
```

## 🔍 Check What's Running

### List All Running Containers
```bash
# Show all running containers
docker ps

# Show all containers (running and stopped)
docker ps -a

# Show containers with specific filters
docker ps --filter "status=running"
```

### Check Port Usage
```bash
# Check what's using specific ports
sudo netstat -tulpn | grep :5555
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :8001
sudo netstat -tulpn | grep :8002
sudo netstat -tulpn | grep :8003

# Or use lsof (on Linux/Mac)
sudo lsof -i :5555
sudo lsof -i :8000-8003

# On Windows, use netstat
netstat -ano | findstr :5555
netstat -ano | findstr :8000
```

## 🧹 Complete Cleanup

### Remove Stopped Containers
```bash
# Remove all stopped containers
docker container prune

# Remove specific containers
docker rm <container_id>

# Force remove running containers
docker rm -f <container_id>
```

### Remove Images (Optional)
```bash
# List all images
docker images

# Remove specific images
docker rmi <image_id>

# Remove all unused images
docker image prune

# Remove all images (careful!)
docker rmi $(docker images -q)
```

### Remove Networks (Optional)
```bash
# List networks
docker network ls

# Remove unused networks
docker network prune

# Remove specific network
docker network rm <network_name>
```

### Complete Docker Cleanup
```bash
# Remove everything (containers, networks, images, build cache)
docker system prune -a

# Remove everything including volumes
docker system prune -a --volumes
```

## 🔧 Specific Port Conflicts

### Kill Processes Using Required Ports
```bash
# Find processes using port 5555 (Coral server)
sudo lsof -i :5555  # Linux/Mac
netstat -ano | findstr :5555  # Windows

# Kill the process
sudo kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Find processes using agent ports (8000-8003)
sudo lsof -i :8000-8003  # Linux/Mac
netstat -ano | findstr :800  # Windows
```

## 🚀 Recommended Cleanup Sequence

### Before Deploying Agent Angus LangChain

1. **Stop all containers:**
   ```bash
   docker stop $(docker ps -q)
   ```

2. **Check for port conflicts:**
   ```bash
   # Linux/Mac
   sudo lsof -i :5555
   sudo lsof -i :8000-8003
   
   # Windows
   netstat -ano | findstr :5555
   netstat -ano | findstr :800
   ```

3. **Kill conflicting processes if needed:**
   ```bash
   # Linux/Mac
   sudo kill -9 <PID>
   
   # Windows
   taskkill /PID <PID> /F
   ```

4. **Clean up Docker resources (optional):**
   ```bash
   docker container prune
   docker network prune
   docker image prune
   ```

5. **Verify ports are free:**
   ```bash
   # Linux/Mac
   sudo lsof -i :5555 :8000 :8001 :8002 :8003
   
   # Windows
   netstat -ano | findstr ":5555 :8000 :8001 :8002 :8003"
   ```

## 🔄 Alternative: Change Ports

If you can't stop certain services, you can change the ports in your `.env` file:

```bash
# Edit .env file
nano .env

# Change these values to unused ports:
CORAL_SERVER_PORT=5556  # Instead of 5555
COORDINATOR_PORT=8010   # Instead of 8000
YOUTUBE_AGENT_PORT=8011 # Instead of 8001
DATABASE_AGENT_PORT=8012 # Instead of 8002
AI_AGENT_PORT=8013      # Instead of 8003
```

## ⚠️ Important Notes

- **Always check what you're stopping** - Some containers might be running important services
- **Use `docker ps` first** to see what's running before stopping everything
- **Consider using different ports** instead of stopping existing services if they're important
- **Make sure to update firewall rules** if you change ports
- **Test the new deployment** after stopping containers to ensure everything works

## 🆘 If Something Goes Wrong

If you accidentally stop something important:

1. **Check Docker Compose files** in other projects to restart services
2. **Look for systemd services** that might need restarting:
   ```bash
   sudo systemctl status docker
   sudo systemctl restart docker
   ```
3. **Check for startup scripts** that might need to be run again
4. **Restart your system** as a last resort to restore default states

---

**Quick Reference:**
- Stop all: `docker stop $(docker ps -q)`
- Check ports: `netstat -tulpn | grep :5555`
- Clean up: `docker system prune`
- Kill process: `sudo kill -9 <PID>` (Linux/Mac) or `taskkill /PID <PID> /F` (Windows)
