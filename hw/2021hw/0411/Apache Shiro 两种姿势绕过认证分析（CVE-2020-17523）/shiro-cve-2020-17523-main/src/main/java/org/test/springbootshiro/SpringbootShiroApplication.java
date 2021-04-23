package org.test.springbootshiro;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping;

/**
 * @author jweny
 */



@SpringBootApplication
public class SpringbootShiroApplication extends SpringBootServletInitializer implements BeanPostProcessor {

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder builder) {
        return builder.sources(SpringbootShiroApplication.class);
    }

    public static void main(String[] args) {

        SpringApplication.run(SpringbootShiroApplication.class, args);
    }

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName)
            throws BeansException {
        if (bean instanceof RequestMappingHandlerMapping) {
            ((RequestMappingHandlerMapping) bean).setAlwaysUseFullPath(true);
        }
        return bean;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName)
            throws BeansException {
        return bean;
    }
}