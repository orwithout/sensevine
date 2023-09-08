cd svelte/ || { echo "svelte/ not found"; exit 1; }
npm run build || { echo "npm run build failed"; exit 1; }
sudo rm -rf /var/www/svelte
cd .. || { echo "cd .. failed"; exit 1; }
sudo cp -rf svelte/public /var/www/svelte
sudo chown -R www-data:www-data /var/www/svelte
sudo chmod -R 755 /var/www/svelte
