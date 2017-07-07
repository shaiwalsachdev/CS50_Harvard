
jQuery(document).ready(function() {
	
    /*
        Fullscreen background
    */
    $.backstretch("static/assets/img/backgrounds/1_1.jpg");
    
    /*
        Login form validation
    */
    $('.login-form input[type="text"], .login-form input[type="password"]').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
    $('.login-form').on('submit', function(e) {
    	
    	$(this).find('input[type="text"], input[type="password"]').each(function(){
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	
    });
    
    /*
        Registration form validation
    */
    $('.registration-form input[type="text"]').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
    $('.registration-form').on('submit', function(e) {
    	
    	$(this).find('input[type="text"]').each(function(){
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	
    	$(this).find('input[type="password"]').each(function(){
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	
    	if ($('#registration input[name=form-password]').val() != $('#registration input[name=form-password1]').val()) 
        {
            alert('passwords don\'t match');
            return false;
        }
        
        
        var email = $('#registration input[name=form-email]').val()  
        
        if(!email.includes(".com"))
        {
            alert('invalid email');
            return false;
        }
        
        if(!email.includes("@"))
        {
            alert('invalid email');
            return false;
        }
    });
    
    
});
