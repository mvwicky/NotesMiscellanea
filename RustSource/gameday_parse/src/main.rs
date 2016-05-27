extern crate xml;
extern crate regex;

use std::fs::File;
use std::io::BufReader;

use xml::reader::{EventReader, XmlEvent};

fn indent(size: usize) -> String {
	const INDENT: &'static str = "    ";
	(0..size).map(|_| INDENT)
		     .fold(String::with_capacity(size*INDENT.len()), |r, s| r + s)
}

fn main() {
    let file = File::open("file.xml").unwrap();
    let file = BufReader::new(file);

    let parser = EventReader::new(file);
    let mut depth = 0;
    for e in parser {
    	match e {
    		Ok(XmlEvent::StartElement {name, ..}) => {
    			println!("{}+{}", indent(depth), name);
    			depth += 1;
    		}
    		Ok(XmlEvent::EndElement { name }) => {
    			depth -= 1;
    			println!("{}-{}", indent(depth), name);
    		}
    		Err(e) => {
    			println!("Error: {}", e);
    			break;
    		}
    		_ => {}
    	}
    }
}
