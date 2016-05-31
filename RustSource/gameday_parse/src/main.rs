extern crate xml;
extern crate regex;

use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
use std::path::Path;

use xml::reader::{EventReader, XmlEvent};

fn indent(size: usize) -> String {
    const INDENT: &'static str = "    ";
    (0..size)
        .map(|_| INDENT)
        .fold(String::with_capacity(size * INDENT.len()), |r, s| r + s)
}

fn main() {
    let retro_path = "E\\retrosheet\\Events";
    let retro_path = Path::new(retro_path);
    let retro_display = retro_path.display();

    let xml_path = Path::new("E:\\gameday_xml\\LAN_2016\\2016-03-03.xml");
    let xml_path = Path::new(xml_path);
    let xml_display = xml_path.display();

    println!("XML Path: {}", xml_display);
    println!("Retrosheet Path: {}", retro_display);

    let xml_file = match File::open(&xml_path) {
        Err(why) => panic!("couldn't open {}:{}", xml_display, why.description()),
        Ok(file) => file,
    };
    let xml_file = BufReader::new(xml_file);

    let parser = EventReader::new(xml_file);
    let mut depth = 0;
    for e in parser {
        match e {
            Ok(XmlEvent::StartElement {name, ..}) => {
                println!("{}+{}", indent(depth), name);
                depth += 1;
            }
            Ok(XmlEvent::EndElement {name}) => {
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
    println!(" ");
}
