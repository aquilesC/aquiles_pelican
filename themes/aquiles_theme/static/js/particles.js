// 3D Particle System with Physics
(function() {
  'use strict';

  if (typeof THREE === 'undefined') {
    return;
  }

  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
    antialias: true,
    powerPreference: 'low-power'
  });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  // Particle configuration
  const PARTICLE_COUNT = prefersReducedMotion ? 120 : 360;
  const PARTICLE_SIZE = 3;
  const GRAVITY = 0.02;
  const DIFFUSION = 0.1;
  const MOUSE_INFLUENCE = 0.4;
  const MOUSE_RADIUS = 250;

  // Warm color palette
  const warmColors = [
    { r: 1.0, g: 0.4, b: 0.2 },
    { r: 1.0, g: 0.6, b: 0.3 },
    { r: 1.0, g: 0.7, b: 0.4 },
    { r: 1.0, g: 0.5, b: 0.3 },
    { r: 0.9, g: 0.3, b: 0.2 },
    { r: 1.0, g: 0.8, b: 0.5 },
    { r: 0.9, g: 0.4, b: 0.3 },
    { r: 1.0, g: 0.6, b: 0.4 }
  ];

  const particleGroup = new THREE.Group();
  const particles = [];
  const velocities = [];

  const sphereGeometry = new THREE.SphereGeometry(PARTICLE_SIZE, 6, 6);

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const radius = Math.random() * 400 + 100;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(Math.random() * 2 - 1);
    
    const x = radius * Math.sin(phi) * Math.cos(theta);
    const y = radius * Math.sin(phi) * Math.sin(theta);
    const z = radius * Math.cos(phi);
    
    velocities.push({
      x: (Math.random() - 0.5) * 0.5,
      y: (Math.random() - 0.5) * 0.5,
      z: (Math.random() - 0.5) * 0.5
    });
    
    const baseColor = warmColors[Math.floor(Math.random() * warmColors.length)];
    const material = new THREE.MeshBasicMaterial({
      color: new THREE.Color(baseColor.r, baseColor.g, baseColor.b),
      transparent: true,
      opacity: 0.7,
      blending: THREE.AdditiveBlending
    });
    
    const sphere = new THREE.Mesh(sphereGeometry, material);
    sphere.position.set(x, y, z);
    
    particles.push(sphere);
    particleGroup.add(sphere);
  }

  scene.add(particleGroup);

  let colorTime = 0;
  const COLOR_SPEED = 0.0005;

  const mouse = new THREE.Vector2();
  const mouseTarget = new THREE.Vector2();
  let mouseActive = false;

  function onPointerMove(clientX, clientY) {
    mouseTarget.x = (clientX / window.innerWidth) * 2 - 1;
    mouseTarget.y = -(clientY / window.innerHeight) * 2 + 1;
    mouseTarget.x *= window.innerWidth * 0.5;
    mouseTarget.y *= window.innerHeight * 0.5;
    mouseActive = true;
  }

  window.addEventListener('mousemove', (e) => onPointerMove(e.clientX, e.clientY), { passive: true });
  window.addEventListener('mouseleave', () => { mouseActive = false; });
  window.addEventListener('touchmove', (e) => {
    if (e.touches && e.touches[0]) {
      onPointerMove(e.touches[0].clientX, e.touches[0].clientY);
    }
  }, { passive: true });
  window.addEventListener('touchend', () => { mouseActive = false; });

  function lerpColor(c1, c2, t) {
    return {
      r: c1.r + (c2.r - c1.r) * t,
      g: c1.g + (c2.g - c1.g) * t,
      b: c1.b + (c2.b - c1.b) * t
    };
  }

  let frame = 0;
  let rafId = null;

  function renderStatic() {
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
  }

  function animate() {
    if (document.hidden) {
      rafId = requestAnimationFrame(animate);
      return;
    }

    rafId = requestAnimationFrame(animate);
    frame++;
    
    colorTime += COLOR_SPEED;
    if (colorTime >= 1) colorTime = 0;

    mouse.lerp(mouseTarget, 0.1);

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const particle = particles[i];
      const vel = velocities[i];
      
      const x = particle.position.x;
      const y = particle.position.y;
      const z = particle.position.z;
      
      const distance = Math.sqrt(x * x + y * y + z * z);
      if (distance > 0.1) {
        const gravityForce = GRAVITY / (distance * distance + 1);
        vel.x -= x * gravityForce;
        vel.y -= y * gravityForce;
        vel.z -= z * gravityForce;
      }
      
      let mouseInteractionStrength = 0;
      if (mouseActive) {
        const mouseDx = mouse.x - x;
        const mouseDy = mouse.y - y;
        const mouseDist = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy + z * z);
        
        if (mouseDist < MOUSE_RADIUS && mouseDist > 0.1) {
          const influence = (MOUSE_RADIUS - mouseDist) / MOUSE_RADIUS;
          const force = MOUSE_INFLUENCE * influence;
          vel.x -= mouseDx * force;
          vel.y -= mouseDy * force;
          vel.z += z * force * 0.5;
          mouseInteractionStrength = influence;
        }
      }
      
      vel.x += (Math.random() - 0.5) * DIFFUSION;
      vel.y += (Math.random() - 0.5) * DIFFUSION;
      vel.z += (Math.random() - 0.5) * DIFFUSION;
      
      vel.x *= 0.98;
      vel.y *= 0.98;
      vel.z *= 0.98;
      
      particle.position.x += vel.x;
      particle.position.y += vel.y;
      particle.position.z += vel.z;
      
      const dist = Math.sqrt(x * x + y * y + z * z);
      if (dist > 600) {
        const scale = 600 / dist;
        particle.position.x *= scale;
        particle.position.y *= scale;
        particle.position.z *= scale;
      }
      
      const colorIndex1 = Math.floor((colorTime + i * 0.001) * warmColors.length) % warmColors.length;
      const colorIndex2 = (colorIndex1 + 1) % warmColors.length;
      const t = ((colorTime + i * 0.001) * warmColors.length) % 1;
      
      let currentColor = lerpColor(warmColors[colorIndex1], warmColors[colorIndex2], t);
      
      if (mouseInteractionStrength > 0) {
        const brightnessBoost = 0.3 * mouseInteractionStrength;
        currentColor = {
          r: Math.min(1, currentColor.r + brightnessBoost),
          g: Math.min(1, currentColor.g + brightnessBoost * 0.8),
          b: Math.min(1, currentColor.b + brightnessBoost * 0.6)
        };
      }
      
      particle.material.color.setRGB(currentColor.r, currentColor.g, currentColor.b);
    }
    
    camera.position.x = Math.sin(frame * 0.001) * 50;
    camera.position.y = Math.cos(frame * 0.0015) * 30;
    camera.lookAt(0, 0, 0);
    
    renderer.render(scene, camera);
  }

  function onResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    if (prefersReducedMotion) {
      renderStatic();
    }
  }

  window.addEventListener('resize', onResize, { passive: true });

  if (prefersReducedMotion) {
    renderStatic();
  } else {
    animate();
  }
})();
