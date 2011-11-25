#!/usr/bin/env ruby



class JsonRPC
	require 'json'
	require 'net/http'
	require 'uri'

	attr_accessor :url, :request_id
	def initialize( url )
		@url = url
		@request_id = 0
	end

	def create_request( method, params )
		req = {
			"id" => request_id,
			"jsonrpc" => "2.0",
			"method" => method,
			"params" => params
			}
		@request_id += 1
		return req
	end

	def call_method( method, params )
		uri = URI.parse( url )
		http = Net::HTTP.new( uri.host, uri.port )
		request = Net::HTTP::Post.new( uri.request_uri )
		request.body = create_request( method, params ).to_json()

		response = http.request( request )
		
		result = JSON.parse( response.body )
		
		if result.include? "error"
			return nil
		end 
		
		return result['result']
	end


end




#client = JsonRPC.new( "http://127.0.0.1:8500/?user=main" )

#print client.call_method( "get_feed", {"feed_url" => 'http://feeds.feedburner.com/TechCrunch/' } ) , "\n"
