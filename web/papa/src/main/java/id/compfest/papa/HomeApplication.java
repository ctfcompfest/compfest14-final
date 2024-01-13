package id.compfest.papa;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

@SpringBootApplication
public class HomeApplication extends SpringBootServletInitializer{
	public static void main(String[] args) {
		SpringApplication.run(HomeApplication.class, args);
	}
}
