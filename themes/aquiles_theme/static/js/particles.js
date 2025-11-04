// 3D Particle System with Physics
(function() {
  'use strict';

  // Check if Three.js is loaded
  if (typeof THREE === 'undefined') {
    console.error('Three.js is required for particle animation');
    return;
  }

  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;

  // Scene setup
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.z = 500;

  const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: true
  });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);

  // Particle system configuration
  const PARTICLE_COUNT = 500; // Reduced count since we're using individual meshes
  const PARTICLE_SIZE = 3;
  const GRAVITY = 0.02;
  const DIFFUSION = 0.1;
  const MOUSE_INFLUENCE = 0.4; // Increased for more evident interaction
  const MOUSE_RADIUS = 250; // Increased radius for more evident interaction

  // Warm color palette (RGB values normalized 0-1)
  const warmColors = [
    { r: 1.0, g: 0.4, b: 0.2 },   // Deep orange
    { r: 1.0, g: 0.6, b: 0.3 },   // Orange
    { r: 1.0, g: 0.7, b: 0.4 },   // Light orange
    { r: 1.0, g: 0.5, b: 0.3 },   // Burnt orange
    { r: 0.9, g: 0.3, b: 0.2 },   // Red-orange
    { r: 1.0, g: 0.8, b: 0.5 },   // Peach
    { r: 0.9, g: 0.4, b: 0.3 },   // Coral
    { r: 1.0, g: 0.6, b: 0.4 },   // Salmon
    { r: 0.8, g: 0.3, b: 0.2 },   // Dark red-orange
    { r: 1.0, g: 0.7, b: 0.5 }    // Light coral
  ];

  // Create spherical particles
  const particleGroup = new THREE.Group();
  const particles = [];
  const velocities = [];
  const baseColors = [];

  // Sphere geometry for particles (reused)
  const sphereGeometry = new THREE.SphereGeometry(PARTICLE_SIZE, 8, 8);

  // Initialize particles as individual meshes
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Random positions in a sphere
    const radius = Math.random() * 400 + 100;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(Math.random() * 2 - 1);
    
    const x = radius * Math.sin(phi) * Math.cos(theta);
    const y = radius * Math.sin(phi) * Math.sin(theta);
    const z = radius * Math.cos(phi);
    
    // Random initial velocities
    velocities.push({
      x: (Math.random() - 0.5) * 0.5,
      y: (Math.random() - 0.5) * 0.5,
      z: (Math.random() - 0.5) * 0.5
    });
    
    // Random base color from warm palette
    const baseColor = warmColors[Math.floor(Math.random() * warmColors.length)];
    baseColors.push(baseColor);
    
    // Create material with warm color
    const material = new THREE.MeshBasicMaterial({
      color: new THREE.Color(baseColor.r, baseColor.g, baseColor.b),
      transparent: true,
      opacity: 0.7,
      blending: THREE.AdditiveBlending
    });
    
    // Create sphere mesh
    const sphere = new THREE.Mesh(sphereGeometry, material);
    sphere.position.set(x, y, z);
    
    particles.push(sphere);
    particleGroup.add(sphere);
  }

  scene.add(particleGroup);

  // Color animation state
  let colorTime = 0;
  const COLOR_SPEED = 0.0005; // Slow color transition speed

  // Mouse tracking
  const mouse = new THREE.Vector2();
  const mouseTarget = new THREE.Vector2();
  let mouseActive = false;

  canvas.addEventListener('mousemove', (event) => {
    mouseTarget.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouseTarget.y = -(event.clientY / window.innerHeight) * 2 + 1;
    mouseTarget.x *= window.innerWidth * 0.5;
    mouseTarget.y *= window.innerHeight * 0.5;
    mouseActive = true;
  });

  canvas.addEventListener('mouseleave', () => {
    mouseActive = false;
  });

  // Touch support for mobile
  canvas.addEventListener('touchmove', (event) => {
    event.preventDefault();
    if (event.touches.length > 0) {
      const touch = event.touches[0];
      mouseTarget.x = (touch.clientX / window.innerWidth) * 2 - 1;
      mouseTarget.y = -(touch.clientY / window.innerHeight) * 2 + 1;
      mouseTarget.x *= window.innerWidth * 0.5;
      mouseTarget.y *= window.innerHeight * 0.5;
      mouseActive = true;
    }
  });

  canvas.addEventListener('touchend', () => {
    mouseActive = false;
  });

  // Helper function to interpolate between colors
  function lerpColor(color1, color2, t) {
    return {
      r: color1.r + (color2.r - color1.r) * t,
      g: color1.g + (color2.g - color1.g) * t,
      b: color1.b + (color2.b - color1.b) * t
    };
  }

  // Animation loop
  let frame = 0;
  function animate() {
    requestAnimationFrame(animate);
    frame++;
    
    // Update color time for smooth transitions
    colorTime += COLOR_SPEED;
    if (colorTime >= 1) colorTime = 0;

    // Smooth mouse interpolation
    mouse.lerp(mouseTarget, 0.1);

    // Update particle positions with physics
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const particle = particles[i];
      const vel = velocities[i];
      
      // Current position
      const x = particle.position.x;
      const y = particle.position.y;
      const z = particle.position.z;
      
      // Gravity toward center
      const centerX = 0;
      const centerY = 0;
      const centerZ = 0;
      
      const dx = centerX - x;
      const dy = centerY - y;
      const dz = centerZ - z;
      
      const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
      
      if (distance > 0.1) {
        const gravityForce = GRAVITY / (distance * distance + 1);
        vel.x += dx * gravityForce;
        vel.y += dy * gravityForce;
        vel.z += dz * gravityForce;
      }
      
      // Enhanced mouse interaction (repel particles more strongly)
      let mouseInteractionStrength = 0;
      if (mouseActive) {
        const mouseDx = mouse.x - x;
        const mouseDy = mouse.y - y;
        const mouseDz = 0 - z; // Mouse is in 2D, so z influence is minimal
        const mouseDist = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy + mouseDz * mouseDz);
        
        if (mouseDist < MOUSE_RADIUS && mouseDist > 0.1) {
          const influence = (MOUSE_RADIUS - mouseDist) / MOUSE_RADIUS;
          const force = MOUSE_INFLUENCE * influence;
          vel.x -= mouseDx * force;
          vel.y -= mouseDy * force;
          vel.z -= mouseDz * force * 0.5;
          
          // Store interaction strength for visual feedback
          mouseInteractionStrength = influence;
        }
      }
      
      // Diffusion (random walk)
      vel.x += (Math.random() - 0.5) * DIFFUSION;
      vel.y += (Math.random() - 0.5) * DIFFUSION;
      vel.z += (Math.random() - 0.5) * DIFFUSION;
      
      // Damping
      vel.x *= 0.98;
      vel.y *= 0.98;
      vel.z *= 0.98;
      
      // Update positions
      particle.position.x += vel.x;
      particle.position.y += vel.y;
      particle.position.z += vel.z;
      
      // Soft boundary (keep particles in view)
      const dist = Math.sqrt(x * x + y * y + z * z);
      if (dist > 600) {
        const scale = 600 / dist;
        particle.position.x *= scale;
        particle.position.y *= scale;
        particle.position.z *= scale;
      }
      
      // Color transition through warm palette
      const colorIndex1 = Math.floor((colorTime + i * 0.001) * warmColors.length) % warmColors.length;
      const colorIndex2 = (colorIndex1 + 1) % warmColors.length;
      const t = ((colorTime + i * 0.001) * warmColors.length) % 1;
      
      let currentColor = lerpColor(warmColors[colorIndex1], warmColors[colorIndex2], t);
      
      // Enhance color when mouse interacts (brighter and more vibrant)
      if (mouseInteractionStrength > 0) {
        const brightnessBoost = 0.3 * mouseInteractionStrength;
        currentColor = {
          r: Math.min(1, currentColor.r + brightnessBoost),
          g: Math.min(1, currentColor.g + brightnessBoost * 0.8),
          b: Math.min(1, currentColor.b + brightnessBoost * 0.6)
        };
      }
      
      // Update particle color
      particle.material.color.setRGB(currentColor.r, currentColor.g, currentColor.b);
      
      // Scale up particles when mouse interacts for more evident feedback
      if (mouseInteractionStrength > 0) {
        const scale = 1 + mouseInteractionStrength * 0.5;
        particle.scale.set(scale, scale, scale);
      } else {
        particle.scale.set(1, 1, 1);
      }
    }
    
    // Rotate camera slowly
    camera.position.x = Math.sin(frame * 0.001) * 50;
    camera.position.y = Math.cos(frame * 0.0015) * 30;
    camera.lookAt(0, 0, 0);
    
    renderer.render(scene, camera);
  }

  // Handle window resize
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  // Respect reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) {
    // Disable animation or make it static
    animate = function() {
      camera.lookAt(0, 0, 0);
      renderer.render(scene, camera);
    };
  }

  // Start animation
  animate();
})();

