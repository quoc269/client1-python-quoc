from flask import Flask, request
from flask.globals import session
from XL_3L_Quan_ly_Don_vi import*
#--THẦY ƠI, DO DUNG LƯỢNG TẬP TIN VƯỢT QUÁ 10M, EM BỎ FOLDER ENVIROMENT FLASK,
#  KHI CHẠY THẦY CÀI LẠI GIÚP EM. CẢM ƠN THẦY!

DichVu = Flask(__name__, static_url_path="/Media", static_folder="Media_QLDV")
DichVu.secret_key = "QuocNguyen" 

#--biến dùng chung

#--Xử lý biến cố khơi động
@DichVu.route("/", methods =["GET"])
def XL_KhoiDong():  
    khungHTML = docKhungHTML() 
    chuoiHTML = Tao_Chuoi_HTML_Dang_nhap()
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)    
    return chuoiHTML

#--Xử lý biến cố đăng nhập của QLDV
@DichVu.route("/QLDV/kiem-tra-dang-nhap", methods =["POST"])
def XL_DangNhapNhanVien():
    khungHTML = docKhungHTML()
    Danh_sach_Quan_ly_Don_vi = Doc_Cong_ty()["Danh_sach_Quan_ly_Don_vi"]
    tenDangNhap = request.form["txtTenDangNhap"]
    matKhau = request.form["txtMatKhau"]
    chuoiHTML =''
    Hop_le = any([QLDV for QLDV in Danh_sach_Quan_ly_Don_vi
                    if QLDV['Ten_Dang_nhap']== tenDangNhap and QLDV['Mat_khau']==matKhau ])
    if Hop_le:
        QLDV = [QLDV for QLDV in Danh_sach_Quan_ly_Don_vi
                          if QLDV['Ten_Dang_nhap']== tenDangNhap and QLDV['Mat_khau']==matKhau][0]       
        Danh_sach_Nhan_vien_Don_vi = Doc_Danh_sach_Nhan_vien_QLDV(QLDV) 
        session['Nguoi_dung'] = QLDV       
       
        Danh_sach_Don_xin_Nghi_QLDV = Doc_Danh_sach_Don_xin_Nghi_QLDV(Danh_sach_Nhan_vien_Don_vi)
        
        chuoiHTML =Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV,Danh_sach_Don_xin_Nghi_QLDV) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_Don_vi) + Tao_Chuoi_HTML_Xem_Quan_ly_Don_vi(QLDV, Danh_sach_Nhan_vien_Don_vi)
    else:
        chuoiHTML = Tao_Chuoi_HTML_Dang_nhap("","","Đăng nhập không hợp lệ")
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
    return chuoiHTML

#--Xử lý chức năng \QLDV\chuc-nang-cap-nhat
@DichVu.route("/QLDV/chuc-nang-cap-nhat", methods=["POST"])
def XL_ChucNangCapNhat_Nhan_vien():
    QLDV ={}   
    if "Nguoi_dung" in session:
        QLDV = session['Nguoi_dung']          
    khungHTML = docKhungHTML() 
    Danh_sach_Nhan_vien_QLDV = Doc_Danh_sach_Nhan_vien_QLDV(QLDV)
    Danh_sach_Don_xin_Nghi_QLDV = Doc_Danh_sach_Don_xin_Nghi_QLDV(Danh_sach_Nhan_vien_QLDV)
    Ma_Xu_ly = request.form["Ma_Xu_ly"]    
    if Ma_Xu_ly == "Cap_nhat_Dien_thoai":
        Ma_so_Nhan_vien = request.form["txtMa_so_Nhan_vien"]  
        Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien_QLDV if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
        sdtMoi = request.form["txtDienThoai"]  
        Nhan_vien["Dien_thoai"] = sdtMoi
        Ghi_Nhan_vien(Nhan_vien)
        chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV,Danh_sach_Don_xin_Nghi_QLDV) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_QLDV) + Tao_Chuoi_HTML_Xem_Quan_ly_Don_vi(QLDV, Danh_sach_Nhan_vien_QLDV)
        chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
    elif Ma_Xu_ly == "Cap_nhat_Dia_chi":
        Ma_so_Nhan_vien = request.form["txtMa_so_Nhan_vien"]  
        Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien_QLDV if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
        Dia_chi = request.form["txtDiaChi"]    
        Nhan_vien["Dia_chi"] = Dia_chi
        Ghi_Nhan_vien(Nhan_vien)
        chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV,Danh_sach_Don_xin_Nghi_QLDV) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_QLDV) + Tao_Chuoi_HTML_Xem_Quan_ly_Don_vi(QLDV, Danh_sach_Nhan_vien_QLDV)
        chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
    elif Ma_Xu_ly == "Cap_nhat_Hinh":
        Ma_so_Nhan_vien = request.form["txtMa_so_Nhan_vien"]  
        Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien_QLDV if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
        Hinh_Nhan_vien = request.files['Hinh_Nhan_vien']
        Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh_Nhan_vien)    
        chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV,Danh_sach_Don_xin_Nghi_QLDV) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_QLDV) + Tao_Chuoi_HTML_Xem_Quan_ly_Don_vi(QLDV, Danh_sach_Nhan_vien_QLDV)
        chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    else:
        Ma_so_Nhan_vien = request.form["txtMa_so_Nhan_vien"]  
        Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien_QLDV if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
        Ma_Ngoai_ngu_Bo_sung = request.form["txtMaNgoaiNgu"]
        Ten_Ngoai_ngu_Bo_sung = request.form["txtTenNgoaiNgu"]
        Ngoai_ngu_Bo_sung = {"Ma_so": Ma_Ngoai_ngu_Bo_sung, "Ten": Ten_Ngoai_ngu_Bo_sung} 
        Nhan_vien["Danh_sach_Ngoai_ngu"].append(Ngoai_ngu_Bo_sung)
        Ghi_Nhan_vien(Nhan_vien)

        chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV,Danh_sach_Don_xin_Nghi_QLDV) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_QLDV) + Tao_Chuoi_HTML_Xem_Quan_ly_Don_vi(QLDV, Danh_sach_Nhan_vien_QLDV)
        chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xử lý biến cố /QLDV/tra-cuu-nhan-vien
@DichVu.route("/QLDV/tra-cuu-nhan-vien", methods=["POST"])
def XL_Tra_cuu_Nhan_vien ():
    khungHTML = docKhungHTML()
    tuKhoa = request.form["txtTuKhoa"]
    QLDV ={}   
    if "Nguoi_dung" in session:
        QLDV = session['Nguoi_dung']
    Danh_sach_Nhan_vien_Don_vi = Doc_Danh_sach_Nhan_vien_QLDV(QLDV)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLDV(Danh_sach_Nhan_vien_Don_vi)  
    Danh_sach_Tim_kiem = Tra_cuu_Quan_ly_Don_vi(QLDV, tuKhoa)
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV, Danh_sach_Don_xin_nghi_Nhan_vien) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Tim_kiem, tuKhoa) + Tao_Chuoi_HTML_Xem_Quan_ly_Don_vi(QLDV, Danh_sach_Tim_kiem)
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xử lý biến cố /QLDV/quan-ly-nhan-vien
@DichVu.route("/QLDV/quan-ly-nhan-vien", methods=["POST"])
def XL_Quan_ly_Nhan_vien():
    khungHTML = docKhungHTML()
    QLDV ={}   
    if "Nguoi_dung" in session:
        QLDV = session['Nguoi_dung']
    Danh_sach_Nhan_vien_Don_vi = Doc_Danh_sach_Nhan_vien_QLDV(QLDV)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLDV(Danh_sach_Nhan_vien_Don_vi)
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV, Danh_sach_Don_xin_nghi_Nhan_vien) + Tao_Chuoi_HTML_Tra_cuu(Danh_sach_Nhan_vien_Don_vi) + Tao_Chuoi_HTML_Xem_Quan_ly_Don_vi(QLDV, Danh_sach_Nhan_vien_Don_vi)
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xử lý duyệt danh sách đơn xin nghỉ /QLDV/duyet-danh-sach-don-xin-nghi
@DichVu.route("/QLDV/duyet-danh-sach-don-xin-nghi", methods=["POST"])
def XL_Duyet_Danh_sach_Don_xin_nghi():
    khungHTML = docKhungHTML()
    QLDV ={}   
    if "Nguoi_dung" in session:
        QLDV = session['Nguoi_dung']
    Danh_sach_Nhan_vien_Don_vi = Doc_Danh_sach_Nhan_vien_QLDV(QLDV)
    Danh_sach_Don_xin_nghi_Nhan_vien = Doc_Danh_sach_Don_xin_Nghi_QLDV(Danh_sach_Nhan_vien_Don_vi) 
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV, Danh_sach_Don_xin_nghi_Nhan_vien) + Tao_Chuoi_HTML_Danh_sach_Don_Xin_nghi(Danh_sach_Don_xin_nghi_Nhan_vien) 
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xử lý duyệt danh sách đơn xin nghỉ /QLDV/duyet-danh-sach-don-xin-nghi
@DichVu.route("/QLDV/duyet-don-xin-nghi", methods=["POST"])
def XL_Duyet_Don_xin_nghi():
    khungHTML = docKhungHTML()   
    QLDV ={}   
    if "Nguoi_dung" in session:
        QLDV = session['Nguoi_dung'] 
    Danh_sach_Nhan_vien_Don_vi = Doc_Danh_sach_Nhan_vien_QLDV(QLDV)   
    Ma_so_Nhan_vien = request.form["txtMa_so_Nhan_vien"]
    Ngay_Nop_don = request.form["txtNgayNop"]  
    Dong_y = request.form["rdbYKien"] 
    Y_kien = False
    Cho_nghi = ""
    Noi_dung = request.form["txtNoiDung"] 
    if Dong_y !="":
        Y_kien = True
    if Dong_y == "Dong_y":
        Cho_nghi = "Đồng ý."
    else:
        Cho_nghi = "Không Đồng ý"
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien_Don_vi if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    for dxn in Nhan_vien["Danh_sach_Don_xin_nghi"]:
        if dxn["Ngay_Nop_don"] == Ngay_Nop_don:
            dxn["Y_kien_Quan_ly_Don_vi"]["Da_co_Y_kien"] = Y_kien
            dxn["Y_kien_Quan_ly_Don_vi"]["Noi_dung"] = Cho_nghi + Noi_dung
    Ghi_Nhan_vien(Nhan_vien)
    session["Nguoi_dung"] = QLDV  
    Danh_sach_Don_xin_nghi_Nhan_vien_moi = Doc_Danh_sach_Don_xin_Nghi_QLDV(Danh_sach_Nhan_vien_Don_vi) 
    chuoiHTML = Tao_Chuoi_HTML_Chuc_Nang_Quan_ly_Don_vi(QLDV, Danh_sach_Don_xin_nghi_Nhan_vien_moi) + Tao_Chuoi_HTML_Danh_sach_Don_Xin_nghi(Danh_sach_Don_xin_nghi_Nhan_vien_moi) 
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    return chuoiHTML

#Xử lý biến cố thoát đăng nhập
@DichVu.route("/Nhan_vien/thoat-dang-nhap", methods=["POST"])
def XL_ThoatDangNhap():
    khungHTML = docKhungHTML()
    if "Nguoi_dung" in session:
        session.pop("Nguoi_dung", None)    
        chuoiHTML = Tao_Chuoi_HTML_Dang_nhap()
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)    
    return chuoiHTML
#--Xóa cache browser
@DichVu.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

#--Run chuong trinh
if __name__ == '__main__':
   DichVu.run()
