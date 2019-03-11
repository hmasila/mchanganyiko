require "rubygems"
require "edfize"
require "csv"

def sample
		edf = Edfize::Edf.new("#{Dir.pwd}/tmp/sample.edf")
		puts edf.class
		# stops the rest of the script if the file is not edf format
		if !validate_format(edf)
			puts "This is not an EDF file"
			return;
		end
		puts "This file has been successfully validated"

		# Loads the data section of the EDF into Signal objects
		edf.load_signals

		headers = ["LABEL", "SAMPLES"]
		
		# Load data to the csv
		csv = CSV.generate(headers: true) do |hdr|
		  edf.signals.each do |signal|
				# data = ["#{signal.label}", "#{signal.samples_per_data_record}"]
				fake = ["kunguni", "kiroboto"]

				hdr << fake
			end
		end
		File.write(path, csv)
		# send_csv
	end

	# edf - the edf object to be validated
	# 
	# Returns boolean

	def validate_format(edf)
		return false if edf.number_of_signals == 0
		true
	end

	def path
		time = (Time.now.strftime '%Y-%m-%d %H:%M:%S').split(" ").join
		"#{Dir.pwd}/tmp/edf2csv#{time}.csv"
	end

	# def filename
	# 	params[:filename].original_filename.split(".").first
	# end

  # def send_csv
  #   send_file @path, type: 'text/csv; charset=utf-8; header=present', disposition: "attachment", filename: File.basename(@path), x_sendfile: true, buffer_size: 512, stream: true
	# end

sample
