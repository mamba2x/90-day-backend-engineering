# Day 30: FastAPI Dependency Injection, Query Parameters and Reusable Filtering

## What I Learned

Today I learned how FastAPI dependency injection works and how reusable logic can be shared between multiple API routes using `Depends()`.

I also learned how to validate query parameters using `Query()` and how multiple filters can be applied sequentially without duplicating logic.

Main concepts covered:

- Dependency injection
- `Depends()`
- Query parameters
- `Query()`
- Query validation
- Optional query parameters
- Reusable filtering logic
- Combining filters
- `completed=False` handling
- Shared dependencies
- OpenAPI documentation
- `/docs`
- `/openapi.json`

---

## Dependency Injection

Dependency injection allows a route to receive something it needs without creating or repeating that logic inside the route itself.

Example:

```python
def get_filtered_tasks():


# Day 30 Completion Checklist

- [x] Understand dependency injection
- [x] Understand why dependencies reduce duplication
- [x] Understand `Depends()`
- [x] Understand why dependencies are passed without `()`
- [x] Understand query parameters
- [x] Understand multiple query parameters
- [x] Understand `Query()`
- [x] Validate query parameters
- [x] Understand `ge` and `le` query validation
- [x] Create a reusable filtering dependency
- [x] Place query parameters in the dependency function signature
- [x] Understand why query declarations do not belong inside the function body
- [x] Start filtering from `tasks.copy()`
- [x] Handle requests with no filters
- [x] Filter by `completed`
- [x] Correctly handle `completed=True`
- [x] Correctly handle `completed=False`
- [x] Understand why `is not None` is required
- [x] Filter by `min_priority`
- [x] Validate minimum priority
- [x] Validate maximum priority
- [x] Combine multiple filters
- [x] Understand AND filtering
- [x] Prevent duplicate filtered results
- [x] Inject dependency into `GET /tasks`
- [x] Understand dependency return values
- [x] Reuse dependency in another endpoint
- [x] Create `/tasks/filtered-count`
- [x] Make both routes depend directly on shared filtering logic
- [x] Correct dependency chaining mistake
- [x] Understand reusable shared logic
- [x] Test no-filter behaviour
- [x] Test `completed=true`
- [x] Test `completed=false`
- [x] Test `min_priority=4`
- [x] Test combined filters
- [x] Test invalid priority query
- [x] Understand OpenAPI
- [x] Understand FastAPI `/docs`
- [x] Understand `/openapi.json`
- [x] Understand how dependencies appear in API documentation
- [x] Review and correct Day 30 mistakes
- [x] Complete Day 30 code review
