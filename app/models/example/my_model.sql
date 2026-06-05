select
    id,
    message,
    loaded_at
from {{ ref('staging_example') }}
