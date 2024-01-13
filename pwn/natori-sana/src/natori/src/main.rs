use libc;
use libc_stdhandle;
use std::io;
use std::process;
use std::os::raw::c_void;

fn main() {
    println!("Enter text: ");
    let mut s = String::new();
    io::stdin().read_line(&mut s);
    unsafe {
        libc::setvbuf(libc_stdhandle::stdout(), &mut 0, libc::_IONBF, 0);

        let text = [0 as libc::c_char; 128].as_mut_ptr();
        if s.chars().count() > 128 {
            println!("No overflowing the buffer...");
            process::exit(-1);
        }
        // libc::strncpy(text, s.as_ptr() as *const libc::c_char, libc::strchr(s.as_ptr() as *const libc::c_char, '\n' as u32) as usize);
        match s.find("\n") {
            None => {
                println!("Something went wrong...");
            }
            Some(length) => {
                libc::memcpy(text as *mut c_void, s.as_ptr() as *const c_void, length); 
                libc::printf("You inputted: %s\0".as_ptr() as *const i8, text);
            }
        }
        
    }
}