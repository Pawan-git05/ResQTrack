// CTA Story Modal Interception and UI Enhancements
(function() {
	const storiesByAction = {
		donate: {
			title: 'Your Donation Heals — Animal Aid Unlimited, Udaipur',
			image: 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?q=80&w=1600&auto=format&fit=crop',
			text: 'Donations funded life-saving treatment for an injured cow. Your support pays for medication, transport, and shelter care so rescues can recover fully.',
			credit: 'Story inspired by Animal Aid Unlimited, Udaipur',
		},
		report: {
			title: 'A Report That Saved a Life — RESQ Trust, Pune',
			image: 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1600&auto=format&fit=crop',
			text: 'A citizen report alerted responders to a buffalo hit by traffic. Rapid coordination ensured safe transport to a hospital for treatment.',
			credit: 'Story inspired by RESQ Charitable Trust, Pune',
		},
		hero: {
			title: 'Become a Hero — People for Animals (PFA)',
			image: 'https://images.unsplash.com/photo-1583336663277-620dc1996580?q=80&w=1600&auto=format&fit=crop',
			text: 'PFA volunteers help goats, dogs, and other animals with pickups, first aid, and fostering. Join the network and make a direct impact.',
			credit: 'Story inspired by People for Animals (PFA)',
		},
	};

	function setupCtaInterception() {
		const modalEl = document.getElementById('storyModal');
		if (!modalEl) return;
		const bsModal = new bootstrap.Modal(modalEl);
		const title = document.getElementById('storyModalTitle');
		const img = document.getElementById('storyModalImage');
		const text = document.getElementById('storyModalText');
		const credit = document.getElementById('storyModalCredit');
		const continueBtn = document.getElementById('storyContinue');
		const backBtn = document.getElementById('storyBack');

		let pendingHref = '#';

		document.querySelectorAll('.cta-intercept').forEach((el) => {
			el.addEventListener('click', (e) => {
				e.preventDefault();
				const action = el.getAttribute('data-action');
				const story = storiesByAction[action];
				pendingHref = el.getAttribute('data-target') || el.getAttribute('href') || '#';
				if (story) {
					title.textContent = story.title;
					img.src = story.image;
					img.alt = story.title;
					text.textContent = story.text;
					credit.textContent = story.credit;
				}
				continueBtn.setAttribute('href', pendingHref);
				bsModal.show();
			});
		});

		backBtn.addEventListener('click', () => {
			bsModal.hide();
		});
	}

	function animateCounters() {
		const targets = window.__resqCounters || { rescues: 0, ngos: 0, volunteers: 0, adoptions: 0 };
		const els = {
			rescues: document.getElementById('count-rescues'),
			ngos: document.getElementById('count-ngos'),
			volunteers: document.getElementById('count-volunteers'),
			adoptions: document.getElementById('count-adoptions'),
		};
		const duration = 1200;
		const start = performance.now();
		function step(now) {
			const progress = Math.min(1, (now - start) / duration);
			Object.entries(els).forEach(([key, el]) => {
				if (!el) return;
				const val = Math.floor(progress * targets[key]);
				el.textContent = String(val);
			});
			if (progress < 1) requestAnimationFrame(step);
		}
		requestAnimationFrame(step);
	}

	function setupRevealOnScroll() {
		const observer = new IntersectionObserver((entries) => {
			entries.forEach((entry) => {
				if (entry.isIntersecting) {
					entry.target.classList.add('revealed');
					observer.unobserve(entry.target);
				}
			});
		}, { threshold: 0.15 });

		document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
	}

	document.addEventListener('DOMContentLoaded', () => {
		setupRevealOnScroll();
		animateCounters();
	});
})();


