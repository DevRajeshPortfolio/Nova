# query_optimizer.py
# Query Optimization for Nova

class QueryOptimizer:
    """Query optimization for database operations"""
    
    def __init__(self):
        self.query_cache = {}
        self.index_suggestions = {}
    
    def optimize_query(self, query: Dict) -> Dict:
        """Optimize a database query"""
        # Add indexes
        optimized = dict(query)
        
        # Use covered queries when possible
        if 'fields' in query and 'index' in query:
            optimized['covered'] = self._can_use_covered_query(query)
        
        # Add hints
        optimized['hints'] = self._add_hints(query)
        
        return optimized
    
    def _can_use_covered_query(self, query: Dict) -> bool:
        """Check if query can use covered indexes"""
        fields = set(query.get('fields', []))
        index_fields = set(query.get('index', []))
        
        # Check if all fields are in the index
        return fields.issubset(index_fields)
    
    def _add_hints(self, query: Dict) -> List:
        """Add query hints"""
        hints = []
        
        # Use index hints
        if 'sort' in query:
            hints.append('USE INDEX (sort_index)')
        
        # Use force index for selective queries
        if 'where' in query:
            hints.append('FORCE INDEX (primary)')
        
        return hints
    
    def analyze_slow_queries(self, slow_queries: List[Dict]):
        """Analyze slow queries and suggest optimizations"""
        for query in slow_queries:
            # Suggest indexes
            if 'where' in query:
                fields = query['where'].keys()
                self.index_suggestions[query.get('collection')] = list(fields)
    
    def get_index_suggestions(self, collection: str) -> List[str]:
        """Get index suggestions for a collection"""
        return self.index_suggestions.get(collection, [])