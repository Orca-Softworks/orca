pub fn starting_1(data_2: u32) -> u32 {
    const data_1: u32 = 10;

    return data_2 * 2 + data_1;
}

pub fn starting_2(data_2: u32) -> u32 {
    const data_1: u32 = 5;

    return data_2 * 4 + data_1;
}

pub intermediate(starting_1: u32, starting_2: u32, internal: u32, feedback_1: u32) -> u32 {
    let new_internal = 3 * starting_1 - internal;

    set!("internal", new_internal);

    return starting_1 + starting_2 - new_internal + feedback_1;
}

pub fn output_1(many_into_one: [10; u32]) -> u32 {
    return many_into_one.sum();
}