package com.psu.Lionchat.api;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

@RequestMapping("/forwardedhandler1")
@RestController
public class Handler1 {
    @GetMapping
    public String getFromHandler1(HttpSession session, HttpServletRequest request)
    {
        System.out.println("Session ID: " + session.getId());
        System.out.println("Session IP: " + request.getRemoteAddr());
        return "This is handler 1's GET request!";
    }

    @PostMapping
    public String postFromHandler1(HttpSession session, HttpServletRequest request)
    {
        System.out.println("Session ID: " + session.getId());
        System.out.println("Session IP: " + request.getRemoteAddr());
        return "This is handler 1's POST request!";
    }
}
