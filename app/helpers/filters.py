from typing import Any, Dict, List, Optional, Type
from sqlalchemy import and_, or_
from sqlalchemy.orm import Query
from pydantic import BaseModel


class FilterOperation:
    EQ = "eq"  # equals
    NE = "ne"  # not equals
    GT = "gt"  # greater than
    LT = "lt"  # less than
    GTE = "gte"  # greater than or equals
    LTE = "lte"  # less than or equals
    LIKE = "like"  # LIKE operation
    IN = "in"  # IN operation
    BETWEEN = "between"  # BETWEEN operation


class FilterParams(BaseModel):
    field: str
    operator: str
    value: Any


def apply_filters(model: Type[Any], query: Query, filters: Optional[List[Dict[str, Any]]] = None) -> Query:
    if not filters:
        return query

    filter_conditions = []
    
    for filter_item in filters:
        filter_params = FilterParams(**filter_item)
        field = getattr(model, filter_params.field, None)
        
        if not field:
            continue

        if filter_params.operator == FilterOperation.EQ:
            filter_conditions.append(field == filter_params.value)
        elif filter_params.operator == FilterOperation.NE:
            filter_conditions.append(field != filter_params.value)
        elif filter_params.operator == FilterOperation.GT:
            filter_conditions.append(field > filter_params.value)
        elif filter_params.operator == FilterOperation.LT:
            filter_conditions.append(field < filter_params.value)
        elif filter_params.operator == FilterOperation.GTE:
            filter_conditions.append(field >= filter_params.value)
        elif filter_params.operator == FilterOperation.LTE:
            filter_conditions.append(field <= filter_params.value)
        elif filter_params.operator == FilterOperation.LIKE:
            filter_conditions.append(field.like(f"%{filter_params.value}%"))
        elif filter_params.operator == FilterOperation.IN:
            filter_conditions.append(field.in_(filter_params.value))
        elif filter_params.operator == FilterOperation.BETWEEN:
            if isinstance(filter_params.value, list) and len(filter_params.value) == 2:
                filter_conditions.append(field.between(filter_params.value[0], filter_params.value[1]))

    if filter_conditions:
        query = query.filter(and_(*filter_conditions))
    
    return query


from typing import Optional
from sqlalchemy.orm import Query
from app.models import Service, ServiceRental

class ServiceFilter:
    @staticmethod
    def apply_filters(query: Query, **filter_params) -> Query:
        filters = []
        
        filter_mapping = {
            'name': {'field': 'name', 'operator': FilterOperation.LIKE},
            'category': {'field': 'category', 'operator': FilterOperation.EQ},
            'min_price': {'field': 'price', 'operator': FilterOperation.GTE},
            'max_price': {'field': 'price', 'operator': FilterOperation.LTE},
            'supplier_id': {'field': 'supplier_id', 'operator': FilterOperation.EQ},
        }

        for param_name, value in filter_params.items():
            if value is not None and param_name in filter_mapping:
                filters.append({
                    'field': filter_mapping[param_name]['field'],
                    'operator': filter_mapping[param_name]['operator'],
                    'value': value
                })

        return apply_filters(Service, query, filters)

class RentalFilter:
    @staticmethod
    def apply_filters(query: Query, **filter_params) -> Query:
        filters = []
        
        filter_mapping = {
            # Rental period filters
            'from_date': {'field': 'from_date', 'operator': FilterOperation.GTE},
            'to_date': {'field': 'to_date', 'operator': FilterOperation.LTE},
            
            # Relationship filters
            'buyer_id': {'field': 'buyer_id', 'operator': FilterOperation.EQ},
            'service_id': {'field': 'service_id', 'operator': FilterOperation.EQ},
            
            # Status filter
            'status': {'field': 'status', 'operator': FilterOperation.EQ},
            
            # Audit timestamp filters
            'created_at_from': {'field': 'created_at', 'operator': FilterOperation.GTE},
            'created_at_to': {'field': 'created_at', 'operator': FilterOperation.LTE},
            'updated_at_from': {'field': 'updated_at', 'operator': FilterOperation.GTE},
            'updated_at_to': {'field': 'updated_at', 'operator': FilterOperation.LTE},
            
            # Additional rental-specific filters
            'is_expired': {'field': 'to_date', 'operator': FilterOperation.LT},  # Filter expired rentals
            'is_active': {'field': 'from_date', 'operator': FilterOperation.LTE}, # Filter currently active rentals
        }

        for param_name, value in filter_params.items():
            if value is not None and param_name in filter_mapping:
                mapping = filter_mapping[param_name]
                filters.append({
                    'field': mapping['field'],
                    'operator': mapping['operator'],
                    'value': value
                })

                # Special case for 'is_active' - needs two conditions
                if param_name == 'is_active' and value:
                    filters.append({
                        'field': 'to_date',
                        'operator': FilterOperation.GTE,
                        'value': datetime.now()
                    })

        return apply_filters(ServiceRental, query, filters)
