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
  const PARTICLE_COUNT = 2000;
  const PARTICLE_SIZE = 2;
  const GRAVITY = 0.02;
  const DIFFUSION = 0.1;
  const MOUSE_INFLUENCE = 0.15;
  const MOUSE_RADIUS = 150;

  // Particle geometry and material
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const velocities = new Float32Array(PARTICLE_COUNT * 3);
  const colors = new Float32Array(PARTICLE_COUNT * 3);

  // Initialize particles
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const i3 = i * 3;
    
    // Random positions in a sphere
    const radius = Math.random() * 400 + 100;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(Math.random() * 2 - 1);
    
    positions[i3] = radius * Math.sin(phi) * Math.cos(theta);
    positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
    positions[i3 + 2] = radius * Math.cos(phi);
    
    // Random initial velocities
    velocities[i3] = (Math.random() - 0.5) * 0.5;
    velocities[i3 + 1] = (Math.random() - 0.5) * 0.5;
    velocities[i3 + 2] = (Math.random() - 0.5) * 0.5;
    
    // Color gradient (cyan to blue)
    const colorIntensity = Math.random() * 0.5 + 0.5;
    colors[i3] = 0.1 * colorIntensity; // R
    colors[i3 + 1] = 0.5 * colorIntensity; // G
    colors[i3 + 2] = 0.8 * colorIntensity; // B
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const material = new THREE.PointsMaterial({
    size: PARTICLE_SIZE,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  });

  const particles = new THREE.Points(geometry, material);
  scene.add(particles);

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

  // Animation loop
  let frame = 0;
  function animate() {
    requestAnimationFrame(animate);
    frame++;

    // Smooth mouse interpolation
    mouse.lerp(mouseTarget, 0.1);

    // Update particle positions with physics
    const positions = geometry.attributes.position.array;
    const velocities_array = velocities;

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const i3 = i * 3;
      
      // Current position
      const x = positions[i3];
      const y = positions[i3 + 1];
      const z = positions[i3 + 2];
      
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
        velocities_array[i3] += dx * gravityForce;
        velocities_array[i3 + 1] += dy * gravityForce;
        velocities_array[i3 + 2] += dz * gravityForce;
      }
      
      // Mouse interaction (repel particles)
      if (mouseActive) {
        const mouseDx = mouse.x - x;
        const mouseDy = mouse.y - y;
        const mouseDz = 0 - z; // Mouse is in 2D, so z influence is minimal
        const mouseDist = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy + mouseDz * mouseDz);
        
        if (mouseDist < MOUSE_RADIUS && mouseDist > 0.1) {
          const influence = (MOUSE_RADIUS - mouseDist) / MOUSE_RADIUS;
          const force = MOUSE_INFLUENCE * influence;
          velocities_array[i3] -= mouseDx * force;
          velocities_array[i3 + 1] -= mouseDy * force;
          velocities_array[i3 + 2] -= mouseDz * force * 0.5;
        }
      }
      
      // Diffusion (random walk)
      velocities_array[i3] += (Math.random() - 0.5) * DIFFUSION;
      velocities_array[i3 + 1] += (Math.random() - 0.5) * DIFFUSION;
      velocities_array[i3 + 2] += (Math.random() - 0.5) * DIFFUSION;
      
      // Damping
      velocities_array[i3] *= 0.98;
      velocities_array[i3 + 1] *= 0.98;
      velocities_array[i3 + 2] *= 0.98;
      
      // Update positions
      positions[i3] += velocities_array[i3];
      positions[i3 + 1] += velocities_array[i3 + 1];
      positions[i3 + 2] += velocities_array[i3 + 2];
      
      // Soft boundary (keep particles in view)
      const dist = Math.sqrt(x * x + y * y + z * z);
      if (dist > 600) {
        const scale = 600 / dist;
        positions[i3] *= scale;
        positions[i3 + 1] *= scale;
        positions[i3 + 2] *= scale;
      }
    }
    
    geometry.attributes.position.needsUpdate = true;
    
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

