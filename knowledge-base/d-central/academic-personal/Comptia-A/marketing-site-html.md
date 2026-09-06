---
source_project: Comptia A+
source_project_uuid: 0196837f-6da6-71e6-954b-c8a742cf2112
doc_uuid: e749351b-2820-4fbb-94d3-8ae16c6dfbb1
original_filename: marketing_site.html
created_at: 2025-04-29T21:45:37.745485+00:00
content_hash: 4ea96fa0024d
topic: comptia-a-learning-platform
consolidated_into: docs/DC-COMPTIA-A-PLATFORM-RECONCILED-001.md
---

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CompTIA A+ Master | Game-Based Learning Platform</title>
    <style>
        :root {
            --primary: #0066cc;
            --primary-dark: #004e9e;
            --secondary: #ff9500;
            --light: #f8f9fa;
            --dark: #343a40;
            --success: #28a745;
            --info: #17a2b8;
            --warning: #ffc107;
            --danger: #dc3545;
            --gray: #6c757d;
            --gray-light: #e9ecef;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background-color: var(--light);
        }
        
        header {
            background-color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        nav {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary);
            text-decoration: none;
            display: flex;
            align-items: center;
        }
        
        .logo-icon {
            margin-right: 0.5rem;
            background-color: var(--primary);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: var(--dark);
            font-weight: 500;
            transition: color 0.2s;
        }
        
        .nav-links a:hover {
            color: var(--primary);
        }
        
        .cta-button {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            text-decoration: none;
        }
        
        .cta-button:hover {
            background-color: var(--primary-dark);
        }
        
        .hero {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 5rem 1rem;
            text-align: center;
        }
        
        .hero-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .hero h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.25rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .hero-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
        }
        
        .secondary-button {
            background-color: transparent;
            color: white;
            border: 2px solid white;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
        }
        
        .secondary-button:hover {
            background-color: rgba(255,255,255,0.1);
        }
        
        .features {
            padding: 5rem 1rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .section-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .section-header h2 {
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }
        
        .section-header p {
            font-size: 1.1rem;
            color: var(--gray);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .feature-card {
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-image {
            width: 100%;
            height: 200px;
            background-color: var(--gray-light);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            font-size: 2rem;
        }
        
        .feature-content {
            padding: 1.5rem;
        }
        
        .feature-content h3 {
            margin-bottom: 0.5rem;
            color: var(--primary);
        }
        
        .feature-content p {
            color: var(--gray);
            margin-bottom: 1rem;
        }
        
        .games {
            background-color: var(--gray-light);
            padding: 5rem 1rem;
        }
        
        .games-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }
        
        .game-card {
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: all 0.3s;
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .game-image {
            width: 100%;
            height: 150px;
            background-color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.25rem;
        }
        
        .game-content {
            padding: 1.5rem;
        }
        
        .game-content h3 {
            margin-bottom: 0.5rem;
            font-size: 1.25rem;
        }
        
        .game-content p {
            font-size: 0.9rem;
            color: var(--gray);
            margin-bottom: 1rem;
        }
        
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            background-color: var(--primary);
            color: white;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-right: 0.5rem;
        }
        
        .pricing {
            padding: 5rem 1rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .pricing-card {
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            padding: 2rem;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        .pricing-card.featured {
            border: 2px solid var(--primary);
            transform: scale(1.05);
        }
        
        .featured-badge {
            position: absolute;
            top: 0;
            right: 0;
            background-color: var(--primary);
            color: white;
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
            font-weight: bold;
            border-bottom-left-radius: 8px;
        }
        
        .price {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 1rem 0;
            color: var(--primary);
        }
        
        .price .period {
            font-size: 1rem;
            color: var(--gray);
            font-weight: normal;
        }
        
        .pricing-card ul {
            list-style: none;
            margin: 1.5rem 0;
            flex-grow: 1;
        }
        
        .pricing-card li {
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
        }
        
        .pricing-card li::before {
            content: "✓";
            color: var(--success);
            margin-right: 0.5rem;
            font-weight: bold;
        }
        
        .pricing-card .cta-button {
            width: 100%;
            text-align: center;
        }
        
        .testimonials {
            background-color: var(--gray-light);
            padding: 5rem 1rem;
        }
        
        .testimonials-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .testimonials-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .testimonial-card {
            background-color: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }
        
        .testimonial-content {
            font-style: italic;
            margin-bottom: 1.5rem;
            position: relative;
        }
        
        .testimonial-content::before {
            content: '"';
            font-size: 4rem;
            position: absolute;
            top: -20px;
            left: -15px;
            color: var(--gray-light);
            z-index: 0;
        }
        
        .testimonial-author {
            display: flex;
            align-items: center;
        }
        
        .author-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: var(--primary);
            margin-right: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .author-info h4 {
            margin-bottom: 0.25rem;
        }
        
        .author-info p {
            font-size: 0.9rem;
            color: var(--gray);
        }
        
        .cta-section {
            padding: 5rem 1rem;
            text-align: center;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .cta-section h2 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: var(--primary);
        }
        
        .cta-section p {
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }
        
        footer {
            background-color: var(--dark);
            color: white;
            padding: 3rem 1rem;
        }
        
        .footer-container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }
        
        .footer-logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }
        
        .footer-links h3 {
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }
        
        .footer-links ul {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 0.75rem;
        }
        
        .footer-links a {
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .footer-links a:hover {
            color: white;
        }
        
        .copyright {
            margin-top: 3rem;
            text-align: center;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.6);
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .hero h1 {
                font-size: 2rem;
            }
            
            .hero p {
                font-size: 1rem;
            }
            
            .hero-buttons {
                flex-direction: column;
                gap: 1rem;
            }
            
            .pricing-card.featured {
                transform: none;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="#" class="logo">
                <div class="logo-icon">A+</div>
                CompTIA A+ Master
            </a>
            <div class="nav-links">
                <a href="#features">Features</a>
                <a href="#games">Games</a>
                <a href="#pricing">Pricing</a>
                <a href="#testimonials">Testimonials</a>
            </div>
            <a href="#" class="cta-button">Start Free Trial</a>
        </nav>
    </header>
    
    <section class="hero">
        <div class="hero-content">
            <h1>Master CompTIA A+ Through Interactive Gaming</h1>
            <p>The most engaging way to prepare for your CompTIA A+ certification. Transform boring study sessions into fun, effective learning experiences.</p>
            <div class="hero-buttons">
                <a href="#" class="cta-button">Start 7-Day Free Trial</a>
                <a href="#" class="secondary-button">View Demo</a>
            </div>
        </div>
    </section>
    
    <section class="features" id="features">
        <div class="section-header">
            <h2>Why Choose CompTIA A+ Master?</h2>
            <p>Our game-based learning platform is designed to make certification prep enjoyable while ensuring you develop practical skills for the real world.</p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-image">🎮</div>
                <div class="feature-content">
                    <h3>Learn by Playing</h3>
                    <p>Transform technical topics into engaging games that make learning enjoyable and effective.</p>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-image">📊</div>
                <div class="feature-content">
                    <h3>Track Your Progress</h3>
                    <p>Detailed analytics identify your strengths and weaknesses across all exam domains.</p>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-image">🧠</div>
                <div class="feature-content">
                    <h3>Adaptive Learning</h3>
                    <p>Our AI-powered system focuses your study time on the areas where you need improvement.</p>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-image">🔄</div>
                <div class="feature-content">
                    <h3>Realistic Simulations</h3>
                    <p>Practice with virtual environments that mimic real-world IT scenarios and problems.</p>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-image">📱</div>
                <div class="feature-content">
                    <h3>Mobile Learning</h3>
                    <p>Study anywhere with our companion app featuring on-the-go activities and review.</p>
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-image">🔒</div>
                <div class="feature-content">
                    <h3>Exam Confidence</h3>
                    <p>Know exactly when you're ready with our certification readiness indicator.</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="games" id="games">
        <div class="games-container">
            <div class="section-header">
                <h2>Our Game Suite</h2>
                <p>Ten interactive games covering every aspect of the CompTIA A+ certification exams.</p>
            </div>
            <div class="games-grid">
                <div class="game-card">
                    <div class="game-image">Tech Trek</div>
                    <div class="game-content">
                        <h3>Tech Trek Challenge</h3>
                        <p>Progress through increasingly difficult questions covering all exam domains.</p>
                        <span class="badge">Core 1</span>
                        <span class="badge">Core 2</span>
                    </div>
                </div>
                <div class="game-card">
                    <div class="game-image">PC Builder</div>
                    <div class="game-content">
                        <h3>PC Builder Workshop</h3>
                        <p>Assemble virtual computers to match specific requirements and budgets.</p>
                        <span class="badge">Hardware</span>
                    </div>
                </div>
                <div class="game-card">
                    <div class="game-image">Network Defense</div>
                    <div class="game-content">
                        <h3>Network Defense</h3>
                        <p>Configure and secure networks against various threats and challenges.</p>
                        <span class="badge">Networking</span>
                        <span class="badge">Security</span>
                    </div>
                </div>
                <div class="game-card">
                    <div class="game-image">IT ER</div>
                    <div class="game-content">
                        <h3>IT Emergency Room</h3>
                        <p>Diagnose and solve technical emergencies under time pressure.</p>
                        <span class="badge">Troubleshooting</span>
                    </div>
                </div>
                <div class="game-card">
                    <div class="game-image">CMD</div>
                    <div class="game-content">
                        <h3>Command Line Conquest</h3>
                        <p>Master command-line interfaces through interactive challenges.</p>
                        <span class="badge">Operating Systems</span>
                    </div>
                </div>
                <div class="game-card">
                    <div class="game-image">Tech Terms</div>
                    <div class="game-content">
                        <h3>Tech Term Titan</h3>
                        <p>Fun mini-games to master terminology, acronyms, and specifications.</p>
                        <span class="badge">All Domains</span>
                    </div>
                </div>
                <div class="game-card">
                    <div class="game-image">Help Desk</div>
                    <div class="game-content">
                        <h3>Support Desk Simulator</h3>
                        <p>Practice professional IT communication and operational procedures.</p>
                        <span class="badge">Operational Procedures</span>
                    </div>
                </div>
                <div class="game-card">
                    <div class="game-image">Security Team</div>
                    <div class="game-content">
                        <h3>Security Response Team</h3>
                        <p>Identify and respond to various security incidents and threats.</p>
                        <span class="badge">Security</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="pricing" id="pricing">
        <div class="section-header">
            <h2>Pricing Plans</h2>
            <p>Choose the package that fits your learning needs and certification timeline.</p>
        </div>
        <div class="pricing-grid">
            <div class="pricing-card">
                <h3>Starter</h3>
                <div class="price">$29.99 <span class="period">/month</span></div>
                <ul>
                    <li>Access to 3 core games</li>
                    <li>Basic progress tracking</li>
                    <li>Limited practice exams</li>
                    <li>Email support</li>
                </ul>
                <a href="#" class="cta-button">Get Started</a>
            </div>
            <div class="pricing-card featured">
                <div class="featured-badge">Most Popular</div>
                <h3>Professional</h3>
                <div class="price">$49.99 <span class="period">/month</span></div>
                <ul>
                    <li>Full access to all 10 learning games</li>
                    <li>Complete progress analytics</li>
                    <li>Unlimited practice exams</li>
                    <li>Mobile companion app</li>
                    <li>Personalized study plans</li>
                    <li>Priority support</li>
                </ul>
                <a href="#" class="cta-button">Get Started</a>
            </div>
            <div class="pricing-card">
                <h3>Premium</h3>
                <div class="price">$149 <span class="period">one-time</span></div>
                <ul>
                    <li>Everything in Professional</li>
                    <li>6 months of unlimited access</li>
                    <li>Exam voucher rebate program</li>
                    <li>Priority technical support</li>
                    <li>Certification preparation e-book</li>
                </ul>
                <a href="#" class="cta-button">Get Started</a>
            </div>
        </div>
    </section>
    
    <section class="testimonials" id="testimonials">
        <div class="testimonials-container">
            <div class="section-header">
                <h2>Success Stories</h2>
                <p>See how CompTIA A+ Master has helped thousands of students achieve certification success.</p>
            </div>
            <div class="testimonials-grid">
                <div class="testimonial-card">
                    <div class="testimonial-content">
                        After struggling with traditional study methods for months, CompTIA A+ Master helped me pass both exams on my first attempt! The games made learning fun, and I actually remembered the material during the exam.
                    </div>
                    <div class="testimonial-author">
                        <div class="author-avatar">MT</div>
                        <div class="author-info">
                            <h4>Michael T.</h4>
                            <p>IT Support Specialist</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-content">
                        As an instructor at a technical college, I've seen a 32% improvement in pass rates since implementing CompTIA A+ Master in our curriculum. Students are more engaged and retain information better through the game-based approach.
                    </div>
                    <div class="testimonial-author">
                        <div class="author-avatar">SJ</div>
                        <div class="author-info">
                            <h4>Dr. Sarah Johnson</h4>
                            <p>IT Department Chair</p>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-content">
                        The simulation games prepared me for real-world scenarios I now face daily in my IT role. This wasn't just exam prep—it was career preparation.
                    </div>
                    <div class="testimonial-author">
                        <div class="author-avatar">DM</div>
                        <div class="author-info">
                            <h4>David M.</h4>
                            <p>Help Desk Technician</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="cta-section">
        <h2>Ready to Transform Your CompTIA A+ Preparation?</h2>
        <p>Join thousands of successful IT professionals who have used our platform to pass their certification exams and advance their careers.</p>
        <a href="#" class="cta-button">Start Your Free 7-Day Trial</a>
        <p style="margin-top: 1rem; font-size: 0.9rem; color: var(--gray);">No credit card required. Cancel anytime.</p>
    </section>
    
    <footer>
        <div class="footer-container">
            <div class="footer-links">
                <div class="footer-logo">
                    <div class="logo-icon" style="width: 30px; height: 30px; font-size: 0.9rem;">A+</div>
                    CompTIA A+ Master
                </div>
                <p>The ultimate game-based learning platform for CompTIA A+ certification.</p>
            </div>
            <div class="footer-links">
                <h3>Product</h3>
                <ul>
                    <li><a href="#">Features</a></li>
                    <li><a href="#">Games</a></li>
                    <li><a href="#">Pricing</a></li>
                    <li><a href="#">Demo</a></li>
                </ul>
            </div>
            <div class="footer-links">
                <h3>Company</h3>
                <ul>
                    <li><a href="#">About Us</a></li>
                    <li><a href="#">Blog</a></li>
                    <li><a href="#">Careers</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </div>
            <div class="footer-links">
                <h3>Resources</h3>
                <ul>
                    <li><a href="#">Help Center</a></li>
                    <li><a href="#">Community</a></li>
                    <li><a href="#">Study Guides</a></li>
                    <li><a href="#">Success Stories</a></li>
                </ul>
            </div>
        </div>
        <div class="copyright">
            <p>&copy; 2025 CompTIA A+ Master. All rights reserved. Not affiliated with or endorsed by CompTIA.</p>
        </div>
    </footer>
</body>
</html>

<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/comptia-a-learning-platform|comptia-a-learning-platform]]

**Consolidated into:**
- [[docs/DC-COMPTIA-A-PLATFORM-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
