#!/usr/bin/env node

/**
 * Helper script to fix v0 components for Create React App
 * Removes "use client" directives and converts TypeScript syntax if needed
 */

const fs = require('fs');
const path = require('path');

const componentsDir = path.join(__dirname, 'src', 'components');

function fixComponent(filePath) {
  if (!fs.existsSync(filePath)) return;
  
  let content = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  
  // Remove "use client" directive
  if (content.includes('"use client"')) {
    content = content.replace(/["']use client["'];?\s*\n?/g, '');
    modified = true;
  }
  
  // Remove "use client" with semicolon
  if (content.includes("'use client'")) {
    content = content.replace(/['"]use client['"];?\s*\n?/g, '');
    modified = true;
  }
  
  if (modified) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓ Fixed: ${path.relative(__dirname, filePath)}`);
  }
}

function walkDir(dir) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      walkDir(filePath);
    } else if (file.endsWith('.jsx') || file.endsWith('.tsx')) {
      fixComponent(filePath);
    }
  });
}

// Run the fix
console.log('Fixing v0 components...\n');
walkDir(componentsDir);
console.log('\nDone!');











