require 'roo'
require 'write_xlsx'
class Excel
	def initialize(file_path)
    @xls = Roo::Spreadsheet.open(file_path)
    # Create a new Excel workbook
		@workbook = WriteXLSX.new("#{Dir.pwd}/tmp/excel_result.xlsx")
	# Add a worksheet
		@worksheet = @workbook.add_worksheet
		@worksheet.set_column(0, 0, 20)
		@worksheet.set_column(0, 1, 20)
		@worksheet.set_column(0, 2, 20)
		@worksheet.set_column(0, 3, 20)
		@worksheet.set_column(0, 4, 20)
  end

  def emails
  	emails = @xls.column(2)
  	names = @xls.column(1)
  	count = 1
  	@worksheet.write(0,   0, "Website")
	@worksheet.write(0,   1, "Company")
	@worksheet.write(0,   2, "First Name")
	@worksheet.write(0,   3, "Last Name")
	@worksheet.write(0,   4, "Email")

  	names.each_with_index do |name, idx|
  		email = emails[idx]
  		website_name = name.split(".com").first
  		website_name = website_name.split(".").map{ |wb| wb.strip.capitalize}.join(" ")
  		if email && count > 2
	  		email_arr = email.split(",")
	  		email_arr.each do |eml|
	  			fullname = eml.split("@").first.split(".")
	  			first_name = fullname.first.strip.capitalize
	  			last_name = fullname[1..-1].map { |ln| ln.strip.capitalize}.join if fullname.size > 1
	  			@worksheet.write(count,   0, name)
	  			@worksheet.write(count,   1, website_name)
	  			@worksheet.write(count,   2, first_name)
	  			@worksheet.write(count,   3, last_name)
	  			@worksheet.write(count,   4, eml)
	  			count+=1
	  		end
	  	else
	  		@worksheet.write(count,   0, name)
	  		@worksheet.write(count,   1, website_name)
	  		count+=1
	  	end
  	end
  	@workbook.close
  end

  def name
  	names = @xls.column(1)
  	names.each do |name|
  		name = name.split(".com").first
  		name = name.split(".").map(&:capitalize).join(" ")
  		worksheet.write(1,   col, "Hi Excel!")
  	end
  end
end

excel = Excel.new("#{Dir.pwd}/tmp/excel.xlsx")
excel.emails