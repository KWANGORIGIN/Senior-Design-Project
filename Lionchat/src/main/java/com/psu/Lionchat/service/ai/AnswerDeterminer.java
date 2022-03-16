package com.psu.Lionchat.service.ai;

import com.google.gson.Gson;
import com.psu.Lionchat.service.chat.requests.ClassifierRequest;
import com.psu.Lionchat.service.chat.requests.SimilarityRequest;
import com.psu.Lionchat.service.chat.responses.ClassifierResponse;
import com.psu.Lionchat.service.chat.responses.SimilarityResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Objects;

@Service
public class AnswerDeterminer implements AnswerDeterminerIF{
    private IntentStrategyIF intentClassifier;
    private StrategyFactory strategyFactory;
    private IntentStrategyIF issueClassifier;

    @Autowired
    /*
    Consider getting rid of this being passed in and create a factory to create IntentStrategyIF
     */
    public AnswerDeterminer()
    {
        strategyFactory = new StrategyFactory();
        issueClassifier = strategyFactory.getStrategy("Flagged_Intent");
    }

    @Override
    public String getAnswer(String question){
        //First check if there is a toxic problem with user's input
        String issueResponse = issueClassifier.doStrategy(question);
        if(Objects.equals(issueResponse, "Valid")){
            String intentType = classifyIntent(question);
            IntentStrategyIF strategy = strategyFactory.getStrategy(intentType);
            return strategy.doStrategy(question);//Returns answer as determined by classifier
        }
        return issueResponse;//Returns error message from issueClassifier
    }

    //Todo: finish implementing this
    private String classifyIntent(String question){
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        Gson gson = new Gson();
        ClassifierRequest utterance = new ClassifierRequest(question);
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> entity = new HttpEntity<String>(gson.toJson(utterance), headers);
        // TODO: make this into a bean.xml / web.xml data source if thats a thing.
        String response = restTemplate.postForObject("http://localhost:8000/intent", entity,
                String.class);
        ClassifierResponse classifierResponse = gson.fromJson(response, ClassifierResponse.class);
        return classifierResponse.getIntent();
    }
}
