package com.psu.Lionchat.service.chat.responses;


import java.util.List;

public class EventResponse {
	private final List<Event> events;
	private final String message;

	public EventResponse(List<Event> events, String message) {
		this.events = events;
		this.message = message;
	}

	public List<Event> getEvents() {
		return this.events;
	}

	public String getMessage() {
		return this.message;
	}

	public String toString() {
		String evts = message;
		for (Event e : events) {
			evts += "<br>" + e.toString();
		}

		return evts;
	}
}

//class Event {
//	private List<String> eventDetails;
//
//	public Event(List<String> eventDetails) {
//		super();
//		this.eventDetails = eventDetails;
//	}
//
//	public List<String> getEventDetails() {
//		return eventDetails;
//	}
//
//	@Override
//	public String toString() {
//		return "Event [eventDetails=" + eventDetails + "]";
//	}
//}