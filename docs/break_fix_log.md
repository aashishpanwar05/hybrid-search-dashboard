# Break and Fix Log

This document records intentional error induction, failure observation, and recovery processes as required for validating debugging skills.

## Error Induction Protocol

For each scenario:
1. **Inject Error**: Describe the intentional change
2. **Observe Failure**: Document symptoms and error messages
3. **Diagnose**: Root cause analysis
4. **Fix**: Solution implementation
5. **Validate**: Confirmation of fix
6. **Prevent**: Future safeguards

## Scenario A: Semantic Index Mismatch

### Inject Error
**Date**: [Date]
**Change**: Modified embedding model in `VectorIndex.__init__()` from `all-MiniLM-L6-v2` to `all-mpnet-base-v2` without rebuilding the vector index.

**Expected Impact**: Dimension mismatch (384 vs 768) causing runtime errors or invalid results.

### Observe Failure
**Symptoms**:
- [Error messages observed]
- [API behavior]
- [Search result quality]

**Logs**:
```
[Error output]
```

### Diagnose
**Root Cause**: Embedding dimensions changed but stored embeddings use old dimensions.

**Evidence**: 
- Model dimension check failed
- Cosine similarity computation errors
- Invalid similarity scores

### Fix
**Solution**: 
1. Added dimension validation in `VectorIndex.__init__()`
2. Added index metadata storage (model name, dimension, build timestamp)
3. Added startup validation in main.py
4. Automatic index rebuild on mismatch

**Code Changes**:
- Modified `backend/app/search/vector.py`
- Modified `backend/app/main.py`
- Added metadata to index files

### Validate
**Tests**:
- Index builds with correct dimensions
- Startup validation catches mismatches
- Automatic rebuild works
- Search results valid

**Metrics**: nDCG@10 recovered to baseline levels

### Prevent
**Safeguards Added**:
- Index metadata validation on load
- Clear error messages for mismatches
- Automatic recovery option
- Documentation of rebuild process

## Scenario B: Schema Migration Break

### Inject Error
**Date**: [Date]
**Change**: Added NOT NULL column `user_agent` to `query_logs` table without migration script.

### Observe Failure
**Symptoms**:
- API fails to log queries
- SQLite constraint errors
- Dashboard shows missing data

### Diagnose
**Root Cause**: Schema mismatch between code expectations and database.

### Fix
**Solution**:
1. Implemented simple migration system
2. Added schema version tracking
3. Backward-compatible column additions
4. Graceful handling of missing columns

### Validate
**Tests**: All logging operations work, data integrity maintained.

### Prevent
**Safeguards**: Migration system prevents schema drift.

## Scenario C: Hybrid Scoring Regression

### Inject Error
**Date**: [Date]
**Change**: Introduced divide-by-zero in `min_max_normalize()` when all scores equal.

### Observe Failure
**Symptoms**: NaN scores, incorrect ranking, evaluation failures.

### Diagnose
**Root Cause**: Edge case not handled in normalization.

### Fix
**Solution**: Added check for uniform scores, return appropriate normalized values.

### Validate
**Tests**: Edge cases covered, evaluation metrics correct.

### Prevent
**Safeguards**: Comprehensive test coverage for edge cases.

## General Lessons Learned

1. **Validation Importance**: Always validate index compatibility on startup
2. **Migration Strategy**: Need systematic approach to schema changes
3. **Edge Case Testing**: Cover normalization edge cases thoroughly
4. **Error Messages**: Clear error messages speed up debugging
5. **Recovery Automation**: Where possible, automate recovery from errors