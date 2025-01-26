
export function currentDateWithOffsetString(offset) {
    const datetime = new Date();
    datetime.setHours(datetime.getHours() + offset);
    return datetime.toISOString().replace("T", " ").slice(0, 19); 
    // Format: "YYYY-MM-DD HH:mm:ss"
  }