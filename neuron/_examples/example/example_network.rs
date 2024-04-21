#[starting_1] {
    const data_1: u32 = 10;

    return data_2 * 2 + data_1;
}

#[starting_2] {
    const data_1: u32 = 5;

    return data_2 * 4 + data_1;
}

#[intermediate] {
    let new_internal = 3 * starting_1 - internal;

    set!("internal", new_internal);

    return starting_1 + starting_2 - new_internal + feedback_1;
}

#[output_1] {
    return many_into_one.sum();
}