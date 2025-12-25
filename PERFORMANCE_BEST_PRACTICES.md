# Performance Best Practices - Quick Reference

## Database Performance

### ✅ DO: Add indexes for filtered/sorted fields
```python
# In model definition
class MyModel(SQLModel, table=True):
    __table_args__ = (
        Index('idx_field_name', 'field_name'),
        Index('idx_composite', 'field1', 'field2'),
    )
```

### ✅ DO: Use select_from for count queries
```python
# Good
stmt = select(func.count()).select_from(Model).where(...)

# Avoid
stmt = select(func.count()).where(...)  # Less efficient
```

### ✅ DO: Optimize connection pools
```python
engine = create_async_engine(
    url,
    pool_size=20,        # Higher for more concurrency
    max_overflow=30,     # Allow burst capacity
    pool_recycle=3600,   # Recycle after 1 hour
    pool_timeout=30,     # Timeout for getting connection
)
```

### ❌ DON'T: Forget to batch operations
```python
# Bad - N+1 queries
for item in items:
    result = await repo.get_by_id(item.id)

# Good - Single query
results = await repo.get_by_ids([item.id for item in items])
```

## Async/Await Performance

### ✅ DO: Use native async clients
```python
# Good
stream = await async_client.stream(...)
async for chunk in stream:
    yield chunk

# Avoid
stream = await asyncio.to_thread(sync_client.stream, ...)
for chunk in stream:  # Blocks event loop
    yield chunk
```

### ✅ DO: Avoid unnecessary async overhead
```python
# Good - No I/O, don't make it async
def build_response(data):
    return Response(**data)

# Avoid - Unnecessary async
async def build_response(data):
    return Response(**data)
```

## Frontend Performance

### ✅ DO: Debounce user inputs
```javascript
import { debounce } from '@/utils/debounce'

// Good
const handleSearch = debounce(() => {
  loadData()
}, 500)

// Avoid - Calls on every keystroke
const handleSearch = () => {
  loadData()  
}
```

### ✅ DO: Use requestAnimationFrame for animations
```javascript
// Good - Smooth 60fps
const animate = () => {
  updateState()
  requestAnimationFrame(animate)
}

// Avoid - Janky, imprecise
const animate = () => {
  updateState()
  setTimeout(animate, 16)
}
```

### ✅ DO: Limit reactive watchers
```javascript
// Good - Debounced storage updates
const saveState = debounce(() => {
  sessionStorage.setItem(KEY, JSON.stringify(state))
}, 1000)

watch(state, saveState, { deep: true })

// Avoid - Saves on every change
watch(state, (newVal) => {
  sessionStorage.setItem(KEY, JSON.stringify(newVal))
}, { deep: true })
```

### ❌ DON'T: Render large lists without optimization
```vue
<!-- Bad - Renders all 10000 items -->
<div v-for="item in allItems" :key="item.id">
  {{ item.name }}
</div>

<!-- Good - Paginated or virtual scroll -->
<div v-for="item in paginatedItems" :key="item.id">
  {{ item.name }}
</div>
```

## Query Optimization

### ✅ DO: Use appropriate pagination
```python
# Good - Limit results
stmt = stmt.offset((page - 1) * size).limit(size)

# Avoid - Loading everything
all_results = await session.exec(stmt).all()
```

### ✅ DO: Use composite indexes wisely
```sql
-- Good for: WHERE is_latest=1 AND status='published'
CREATE INDEX idx_latest_status ON prompt (is_latest, status);

-- Also good for: WHERE is_latest=1 (uses prefix)

-- Won't help: WHERE status='published' (not leftmost)
```

## Caching Strategies

### When to Cache
- ✅ Frequently accessed data
- ✅ Expensive computations
- ✅ Rarely changing data
- ❌ User-specific data
- ❌ Real-time data
- ❌ Large objects (>1MB)

### Example: Simple Memory Cache
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_config(key: str):
    # Expensive operation
    return fetch_from_db(key)
```

## Performance Monitoring

### Backend Metrics to Track
```python
# Request duration
@app.middleware("http")
async def add_metrics(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"Request duration: {duration:.3f}s")
    return response
```

### Frontend Metrics
```javascript
// Page load time
performance.mark('page-load-start')
// ... page loads
performance.mark('page-load-end')
performance.measure('page-load', 'page-load-start', 'page-load-end')
```

## Common Pitfalls

### 1. Deep Object Comparison
```javascript
// Bad - Deep comparison on every render
const isEqual = computed(() => JSON.stringify(obj1) === JSON.stringify(obj2))

// Good - Track specific fields
const isEqual = computed(() => obj1.id === obj2.id && obj1.name === obj2.name)
```

### 2. Unnecessary Re-renders
```vue
<!-- Bad - Creates new function every render -->
<button @click="() => handleClick(item.id)">

<!-- Good - Use method reference -->
<button @click="handleClick(item.id)">
```

### 3. Blocking Operations
```python
# Bad - Blocks event loop
def process_large_file():
    return open('huge.txt').read()

# Good - Use async
async def process_large_file():
    async with aiofiles.open('huge.txt') as f:
        return await f.read()
```

## Quick Wins Checklist

- [ ] Database indexes on filtered/sorted columns
- [ ] Connection pool optimization (20/30 connections)
- [ ] Debounce search inputs (300-500ms)
- [ ] Use requestAnimationFrame for animations
- [ ] Paginate large datasets
- [ ] Use native async clients
- [ ] Cache expensive operations
- [ ] Monitor slow queries (>100ms)
- [ ] Optimize bundle size (<500KB gzipped)
- [ ] Lazy load components

## Performance Budget

Recommended targets:
- **Page Load**: <2s (initial), <500ms (subsequent)
- **API Response**: <200ms (p95)
- **Database Query**: <50ms (p95)
- **Search Response**: <300ms with debouncing
- **Animation Frame Rate**: 60fps (16.67ms/frame)
- **Memory**: <100MB frontend, <500MB backend per worker

## Tools

### Backend
```bash
# Profile Python code
python -m cProfile -o output.prof script.py

# Analyze queries
SET profiling = 1;
SELECT * FROM prompt WHERE ...;
SHOW PROFILES;
```

### Frontend
```javascript
// Chrome DevTools Performance tab
// Network tab for bundle analysis
// Lighthouse for overall score

// Manual timing
console.time('operation')
// ... code
console.timeEnd('operation')
```

## References

- Database Indexes: See `PERFORMANCE_IMPROVEMENTS.md`
- Migration Guide: See `OPTIMIZATION_SUMMARY.md`
- Full Details: See PR description

---

**Last Updated**: 2025-12-25
**Maintained by**: Development Team
