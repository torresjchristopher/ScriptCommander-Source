# Project Nemo - Tier 2 Quick Reference

## Location Map

| Layer | Name | Path | Key Class |
|-------|------|------|-----------|
| 3 | Statistical Pattern | Mercury Analytics | `PatternEngine` |
| 4 | Context Manager | Challenger Discovery | `ContextManager` |
| 5 | Action Orchestrator | Discovery DevOps | `EventOrchestrator` |
| 6 | E-Commerce Intent | Challenger Discovery | `ECommerceEngine` |
| 7 | Mobile Context | Liberty Mobile | `MobileAdapter` |
| 8 | Security Threat | Freedom Crypto | `ThreatDetector` |
| 9 | Experience Layer | Stargate Graphics | `ExperienceEngine` |
| 10 | GraphQL API | Excelsior Web3 | `GraphQLEngine` |
| 11 | PWA Suite | Liberty Mobile | `PWAManager` |

## Quick Start

### Layer 3 - Pattern Recognition
```bash
cd Project-Mercury-Data-Science-Analytics/programs/task-3-statistical-patterns/
pip install -r requirements.txt
python cli.py analyze login browse checkout logout
python cli.py predict --top-k 5 login browse checkout
```

### Layer 4 - Context Management
```bash
cd Project-Challenger-Discovery-S/programs/task-4-context-manager/
pip install -r requirements.txt
python cli.py create_context user_123
python cli.py set_value user_123 action login
python cli.py get_context user_123
```

### Layer 5 - Orchestration
```bash
cd Project-Discovery-DevOps-Cloud-Infrastructure/programs/task-5-action-orchestrator/
pip install -r requirements.txt
python cli.py process_events login checkout logout
python cli.py execute_actions auth payment confirmation
```

### Layer 6 - E-Commerce
```bash
cd Project-Challenger-Discovery-S/programs/task-6-ecommerce-intent/
pip install -r requirements.txt
python cli.py classify_intent browse
python cli.py add_to_cart --product-id p123 --price 29.99
```

### Layer 7 - Mobile Context
```bash
cd Project-Liberty-Mobile-Development/programs/task-7-mobile-context/
pip install -r requirements.txt
python cli.py detect_device iPhone
python cli.py adapt_response --device-type mobile
```

### Layer 8 - Security
```bash
cd Project-Freedom-Security-Cryptography/programs/task-8-threat-detector/
pip install -r requirements.txt
python cli.py score_threat --ip 192.168.1.1 --velocity high
python cli.py match_patterns --ip 10.0.0.1
```

### Layer 9 - Experience
```bash
cd Project-Stargate-Game-Development-Graphics/programs/task-9-experience-layer/
pip install -r requirements.txt
python cli.py track_interaction click
python cli.py calc_ux_score --response-time 250
```

### Layer 10 - GraphQL
```bash
cd Project-Excelsior-Blockchain-Web3/programs/task-10-graphql-layer/
pip install -r requirements.txt
python cli.py validate_query "{ user { id } }"
python cli.py execute_query "{ user(id: \"123\") { id } }"
```

### Layer 11 - PWA
```bash
cd Project-Liberty-Mobile-Development/programs/task-11-pwa-suite/
pip install -r requirements.txt
python cli.py build_manifest "My App"
python cli.py setup_caching network-first
```

## Python API Usage

### Pattern Recognition
```python
from pattern_engine import create_engine
engine = create_engine(order=2, sensitivity=0.7)
metrics = engine.process_event_stream(['login', 'browse', 'checkout'])
print(metrics.anomaly_score)
predictions = engine.get_next_state_predictions(['login', 'browse'])
```

### Context Management
```python
from context_engine import create_manager
manager = create_manager()
manager.create_context("user_1", {"ip": "192.168.1.1"})
manager.set_context_value("user_1", "action", "login")
manager.correlate_contexts("session_1", "session_2")
context = manager.get_full_context("user_1")
```

### Event Orchestration
```python
from action_orchestrator import create_orchestrator
orch = create_orchestrator()
results = orch.process_events(['login', 'browse', 'add_to_cart', 'checkout'])
state = orch.get_current_state()
orch.execute_actions(['send_email', 'log_event', 'update_analytics'])
```

### E-Commerce
```python
from ecommerce_intent import create_engine
engine = create_engine()
intent = engine.classify_intent(['browse', 'add_to_cart', 'checkout'])
cart = engine.create_cart("user_123")
engine.add_to_cart(cart, "product_1", quantity=1, price=29.99)
clv = engine.calculate_clv(["order1", "order2"], [100, 150])
```

### Mobile Context
```python
from mobile_context import create_adapter
adapter = create_adapter()
device = adapter.detect_device("Mozilla/5.0 (iPhone...")
optimized = adapter.optimize_response({"data": [1,2,3]}, "mobile", "4g")
location = adapter.get_location("lat", "lon")
```

### Security
```python
from threat_detector import create_detector
detector = create_detector()
score = detector.score_threat(ip="192.168.1.1", velocity="high")
detector.update_baseline(ip="10.0.0.1", velocity="normal")
match = detector.match_patterns(ip="10.0.0.1", pattern="brute_force")
```

### Experience
```python
from experience_layer import create_engine
engine = create_engine()
engine.track_interaction("user_1", "click", target="button")
ux_score = engine.calculate_ux_score(error_count=1, response_time=250)
frustration = engine.detect_frustration(errors=2, retries=3)
```

### GraphQL
```python
from graphql_layer import create_engine
engine = create_engine()
schema = engine.get_schema()
result = engine.execute_query("{ users { id name } }")
mutation_result = engine.execute_mutation("mutation { updateUser(...) }")
```

### PWA
```python
from pwa_suite import create_manager
manager = create_manager()
manifest = manager.build_manifest(name="App", icon="/icon.png")
manager.setup_caching_strategy("network-first")
manager.queue_sync("sync:data", {"data": "payload"})
```

## Performance Targets

| Layer | Operation | Target | Typical |
|-------|-----------|--------|---------|
| 3 | Pattern scoring | < 10ms | 5-8ms |
| 4 | Session get/set | < 1ms | 0.5ms |
| 5 | Event processing | < 20ms | 15ms |
| 6 | Intent classification | < 10ms | 7ms |
| 7 | Device detection | < 5ms | 3ms |
| 8 | Threat scoring | < 25ms | 20ms |
| 9 | UX scoring | < 20ms | 15ms |
| 10 | Query execution | < 30ms | 20ms |
| 11 | Manifest gen | < 5ms | 2ms |

## Integration Examples

### User Login Flow
```python
# Pattern: Recognize login pattern
pattern_engine.process_event_stream(['login'])

# Context: Create session
context_manager.create_context('user_123')

# Orchestration: Route through login workflow
orchestrator.process_events(['login'])

# Security: Check threat
threat_detector.score_threat(ip=request.ip)

# Experience: Track UX
experience.track_interaction('user_123', 'login_complete')

# GraphQL: Return unified response
graphql.execute_query("{ user { id session { state } } }")
```

### Mobile Product Purchase
```python
# Mobile: Adapt response for device
mobile.optimize_response(response, device_type='mobile')

# E-Commerce: Classify shopping intent
ecommerce.classify_intent(['browse', 'add_to_cart', 'checkout'])

# Pattern: Detect anomalies
pattern_engine.process_event_stream(['login', 'browse', 'checkout'])

# Experience: Track satisfaction
experience.track_interaction('user_123', 'purchase_complete')

# PWA: Cache for offline
pwa.queue_sync('order_placement', order_data)
```

## Configuration Defaults

| Layer | Config | Default | Range |
|-------|--------|---------|-------|
| 3 | Order | 2 | 1-5 |
| 3 | Sensitivity | 0.7 | 0.0-1.0 |
| 4 | Max sessions | 10000 | 1000-100000 |
| 4 | TTL (seconds) | 3600 | 60-86400 |
| 5 | Queue size | 1000 | 100-10000 |
| 6 | Cart timeout | 1800 | 300-3600 |
| 7 | Cache size | 100 | 10-1000 |
| 8 | Baseline window | 1000 | 100-10000 |
| 9 | Session window | 10000 | 1000-100000 |
| 10 | Cache size | 500 | 50-5000 |
| 11 | Cache version | v1.0.0 | semantic |

## Monitoring Endpoints

Each layer provides statistics via CLI:

```bash
# Layer 3
python cli.py export_model | grep "total_transitions"

# Layer 4
python cli.py stats

# Layer 5
python cli.py stats

# Layer 6
python cli.py stats

# Layer 7
python cli.py stats

# Layer 8
python cli.py stats

# Layer 9
python cli.py stats

# Layer 10
python cli.py stats

# Layer 11
python cli.py stats
```

## Troubleshooting

### Common Issues

**Issue:** Import errors
```bash
pip install -r requirements.txt
```

**Issue:** Permission denied
```bash
chmod +x *.py
```

**Issue:** Port already in use (for potential server modes)
```bash
# Check which process is using the port
lsof -i :PORT
kill -9 PID
```

**Issue:** Memory usage high
- Reduce max_sessions/max_memory in configs
- Increase cleanup frequency
- Monitor with `stats` commands

## Git Repository Maintenance

All layers are git-initialized. Common operations:

```bash
# Check status
git status

# View commit history
git log --oneline

# Make changes
git add .
git commit -m "Description of changes"

# Push to remote (when set up)
git push origin master
```

## Documentation

Each layer includes comprehensive README with:
- Architecture overview
- Component descriptions
- Usage examples
- Performance characteristics
- Integration points
- API reference
- Troubleshooting guide

Read individual READMEs for detailed information:
```bash
cat task-3-statistical-patterns/README.md
cat task-4-context-manager/README.md
# ... etc
```

## Resources

- **Full Build Summary:** `NEMO_TIER2_BUILD_COMPLETE.md`
- **Individual READMEs:** See each layer directory
- **Code:** See each `*_engine.py` or `*_detector.py` file
- **CLI Help:** `python cli.py --help` in any layer

## Support

For questions about:
- **Specific layer:** Check that layer's README
- **Integration:** See NEMO_TIER2_BUILD_COMPLETE.md data flow section
- **API:** Check docstrings in core module
- **Performance:** Check README performance section

---

**Build Date:** January 29, 2026
**Build Status:** ✅ COMPLETE
**Total Layers:** 9
**Total LOC:** 3,550+
