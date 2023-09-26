require 'httparty'
require 'base64'

class QueriesController < ApplicationController
    skip_before_action :verify_authenticity_token, only: [:test_query]

    def new
      @query_data = { greeting: "Hello, React!" }
    end

    def test_query
      pdf_data = params[:pdf_data].read
      question = params[:question]
      pdf_data_base64 = Base64.encode64(pdf_data)

      response = HTTParty.post("http://127.0.0.1:5000/test_query",
                    body: { pdf_data: pdf_data_base64, question: question }.to_json,
                    headers: { 'Content-Type' => 'application/json' })

      render json: { message: "Test query from Rails app", flask_response: response.parsed_response }, status: :ok
    rescue => e
      render json: { message: "Error processing test query", error: e.message }, status: :bad_request
    end
  end
