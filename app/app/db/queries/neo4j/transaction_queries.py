CREATE_TRANSACTION = """
    CREATE (t:Transaction {
        block_id: $block_id,
        hash: $hash,
        time: datetime($time),
        size: $size,
        weight: $weight,
        version: $version,
        lock_time: $lock_time,
        is_coinbase: $is_coinbase,
        has_witness: $has_witness,
        input_count: $input_count,
        output_count: $output_count,
        input_total: $input_total,
        input_total_usd: $input_total_usd,
        output_total: $output_total,
        output_total_usd: $output_total_usd,
        fee: $fee,
        fee_usd: $fee_usd,
        fee_per_kb: $fee_per_kb,
        fee_per_kb_usd: $fee_per_kb_usd,
        fee_per_kwu: $fee_per_kwu,
        fee_per_kwu_usd: $fee_per_kwu_usd,
        cdd_total: $cdd_total
    }) RETURN t
"""

BULK_CREATE_TRANSACTIONS = """
    UNWIND $transactions AS tx
    CREATE (t:Transaction {
        block_id: tx.block_id,
        hash: tx.hash,
        time: datetime(tx.time),
        size: tx.size,
        weight: tx.weight,
        version: tx.version,
        lock_time: tx.lock_time,
        is_coinbase: tx.is_coinbase,
        has_witness: tx.has_witness,
        input_count: tx.input_count,
        output_count: tx.output_count,
        input_total: tx.input_total,
        input_total_usd: tx.input_total_usd,
        output_total: tx.output_total,
        output_total_usd: tx.output_total_usd,
        fee: tx.fee,
        fee_usd: tx.fee_usd,
        fee_per_kb: tx.fee_per_kb,
        fee_per_kb_usd: tx.fee_per_kb_usd,
        fee_per_kwu: tx.fee_per_kwu,
        fee_per_kwu_usd: tx.fee_per_kwu_usd,
        cdd_total: tx.cdd_total
    })
    RETURN t
"""

GET_TRANSACTION = """
    MATCH (t:Transaction {hash: $hash}) RETURN t
"""
