use std::io::Read;
use encoding_rs::Encoding;

use crate::constants::BUFFER_SIZE;


pub struct CsvParser {
    pub delimiter: u8,
    pub quote_char: u8,
    pub encoding: &'static Encoding,
}


impl CsvParser {
    pub fn new(
        delimiter: u8,
        quote_char: u8,
        encoding: &'static Encoding,
    ) -> Self {
        CsvParser {
            delimiter,
            quote_char,
            encoding,
        }
    }

    pub fn read_row_from_buffer<R: Read>(
        &self,
        reader: &mut R,
        buffer: &mut Vec<u8>,
        pos: &mut usize,
        eof: &mut bool,
    ) -> Result<Option<Vec<String>>, String> {
        let mut row = Vec::new();
        let mut field = Vec::new();
        let mut in_quotes = false;
        let mut at_start = true;

        loop {
            if *pos >= buffer.len() {
                if *eof {
                    if !field.is_empty() || !at_start {
                        row.push(self.field_to_string(&field));
                    }
                    if row.is_empty() {
                        return Ok(None);
                    }
                    return Ok(Some(row));
                }

                buffer.clear();
                buffer.resize(BUFFER_SIZE, 0);

                match reader.read(&mut buffer[..]) {
                    Ok(0) => {
                        *eof = true;
                        buffer.clear();
                        if !field.is_empty() || !at_start {
                            row.push(self.field_to_string(&field));
                        }
                        if row.is_empty() {
                            return Ok(None);
                        }
                        return Ok(Some(row));
                    }
                    Ok(n) => {
                        buffer.truncate(n);
                        *pos = 0;
                    }
                    Err(e) => return Err(format!("Read error: {}", e)),
                }
            }

            let byte = buffer[*pos];
            *pos += 1;
            at_start = false;

            if byte == self.quote_char {
                if in_quotes {
                    if *pos < buffer.len() &&
                        buffer[*pos] == self.quote_char {
                        field.push(self.quote_char);
                        *pos += 1;
                        continue;
                    } else {
                        in_quotes = false;
                        continue;
                    }
                } else {
                    in_quotes = true;
                    continue;
                }
            }

            if !in_quotes && byte == self.delimiter {
                row.push(self.field_to_string(&field));
                field.clear();
                continue;
            }

            if !in_quotes && (byte == b'\n' || byte == b'\r') {
                if byte == b'\r' {
                    continue;
                }

                row.push(self.field_to_string(&field));
                field.clear();

                return Ok(Some(row));
            }

            field.push(byte);
        }
    }

    fn field_to_string(&self, field: &[u8]) -> String {
        if field.is_empty() {
            return String::new();
        }

        let (cow, _, _) = self.encoding.decode(field);
        cow.to_string()
    }
}
